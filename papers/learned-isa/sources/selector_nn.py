"""Independent small MLP selectors with the same decoded information as PAN."""
import torch
from torch import nn

from isa_lab.full_models import HEAD_SIZES, TrainableSelectors
from pan_isa.native import runtime_module, stages


class StageHead(nn.Module):
    def __init__(self, count, outputs, has_flags):
        super().__init__()
        self.has_flags = has_flags
        self.embedding = nn.Embedding(count, 16)
        self.trunk = nn.Sequential(nn.Linear(16 + (4 if has_flags else 0), 64), nn.GELU())
        self.outputs = nn.ModuleList(nn.Linear(64, n) for n in outputs)

    def selector_logits(self, ops, flags=None):
        x = self.embedding(ops)
        if self.has_flags:
            x = torch.cat((x, flags), -1)
        return tuple(h(self.trunk(x)) for h in self.outputs)

    def forward(self, ops, flags=None):
        return self.selector_logits(ops, flags)[0]


class RuntimeHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(256, 8)
        self.net = nn.Sequential(nn.Linear(120 + len(runtime_module().NUMERIC_FEATURE_NAMES), 64),
                                 nn.GELU(), nn.Linear(64, 33))

    def forward(self, raw, numeric):
        return self.net(torch.cat((self.embedding(raw).flatten(1), numeric), -1))


class FullNNSelectors(TrainableSelectors):
    name = "nn"
    implementation = "small-mlp-pan-full-scope-selectors-v1"

    def __init__(self, seed=17):
        super().__init__()
        torch.manual_seed(seed)
        self.heads = nn.ModuleDict({str(i): StageHead(len(s.OPS), HEAD_SIZES[i], i in (2, 3))
                                    for i, s in enumerate(stages())})
        self.heads["runtime"] = RuntimeHead()
