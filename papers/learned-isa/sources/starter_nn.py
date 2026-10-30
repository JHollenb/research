from __future__ import annotations

import torch
from torch import nn

from isa_lab.contracts import ACTIONS, State
from isa_lab.profile import instruction_key, proposal


class NNSelector(nn.Module):
    name = "nn"
    implementation = "byte-embedding-mlp-selector-v1"

    def __init__(self, seed=17, device="cpu"):
        super().__init__()
        torch.manual_seed(seed)
        self.embedding = nn.Embedding(256, 8)
        self.head = nn.Sequential(nn.Linear(23, 64), nn.GELU(), nn.Linear(64, len(ACTIONS)))
        self.to(device)

    def features(self, instruction, before):
        # Full observed instruction bytes and the same typed before-state available to all arms.
        padded = list(instruction) + [0] * (2 - len(instruction))
        return padded, [len(instruction) / 2, before.al / 255, before.bl / 255,
                        before.cf, before.zf, before.sf, before.of]

    def logits(self, instructions, states):
        encoded = [self.features(i, s) for i, s in zip(instructions, states, strict=True)]
        device = next(self.parameters()).device
        tokens = torch.tensor([row[0] for row in encoded], dtype=torch.long, device=device)
        context = torch.tensor([row[1] for row in encoded], dtype=torch.float32, device=device)
        return self.head(torch.cat((self.embedding(tokens).flatten(1), context), dim=1))

    def update(self, observations, routes, optimizer):
        self.train()
        instructions = [bytes.fromhex(row["instruction"]) for row in observations]
        states = [State.from_dict(row["before"]) for row in observations]
        labels = torch.tensor([ACTIONS.index(routes[instruction_key(i).hex()]) for i in instructions],
                              device=next(self.parameters()).device)
        optimizer.zero_grad(set_to_none=True)
        loss = nn.functional.cross_entropy(self.logits(instructions, states), labels)
        loss.backward()
        optimizer.step()
        return {"loss": float(loss.detach().cpu()), "physical_examples": len(observations)}

    def discovery_loss(self, observations, routes):
        """Discovery-only progress signal after discrete consumer scores saturate."""
        instructions = [bytes.fromhex(row["instruction"]) for row in observations]
        states = [State.from_dict(row["before"]) for row in observations]
        labels = torch.tensor([ACTIONS.index(routes[instruction_key(i).hex()]) for i in instructions],
                              device=next(self.parameters()).device)
        with torch.no_grad():
            return float(nn.functional.cross_entropy(self.logits(instructions, states), labels).cpu())

    def propose(self, instruction, before):
        instruction_key(instruction)
        with torch.no_grad():
            logits = self.logits([instruction], [before])[0]
            action = ACTIONS[int(logits.argmax())]
        return proposal(action, instruction, before, {"action": action, "logits": logits.cpu().tolist()})

    def export(self):
        return {"implementation": self.implementation,
                "weights": {key: value.detach().cpu().tolist() for key, value in self.state_dict().items()},
                "parameter_count": sum(p.numel() for p in self.parameters())}

    def restore_export(self, artifact):
        self.load_state_dict({key: torch.tensor(value, dtype=self.state_dict()[key].dtype)
                              for key, value in artifact["weights"].items()})
