"""Native packed SPF multi-axis reads spanning the PAN instruction inventory."""
import json

import numpy as np

from isa_lab.dependencies import spf_modules
from isa_lab.full_models import StructuralSelectors


class FullSPFSelectors(StructuralSelectors):
    name = "spf_transformer"
    implementation = "spf-native-pan-full-scope-phase-memory-v1"

    def address(self, key):
        codes = np.array(list(key) + [0] * (9 - len(key)), dtype=np.uint16).reshape(1, 9)
        # All addresses fit in 9 integer phase channels (largest op index 267).
        words = self.core.pack_words(np.zeros((1, 9), dtype=np.int16), codes * 128)
        return self.circuits.execute_phase_character_features(words,
                    characters=tuple(((i, 1),) for i in range(9)))

    def prepare(self):
        self.core, self.circuits, self.select = spf_modules()
        entries = sorted(self.routes.items())
        self.keys = np.concatenate([self.address(json.loads(k)) for k, _ in entries]) if entries else np.empty((0, 9), dtype=np.uint32)
        values = np.array([list(v) + [0] * (4 - len(v)) for _, v in entries], dtype=np.uint16).reshape(-1, 4)
        self.values = self.core.pack_words(np.zeros(values.shape, dtype=np.int16), (values + 1) * 128)

    def read(self, key):
        if not len(self.keys):
            raise ValueError("empty phase memory")
        result = self.select.execute_select_head(self.address(key), self.keys, self.values,
                    channel_weights=np.ones(9, dtype=np.int64), score="exact_match", min_score=9, causal=False)
        if not bool(result.found[0, 0]):
            raise ValueError(f"missing phase route: {key}")
        return ((self.core.unpack_theta(result.values)[0, 0] // 128).astype(int) - 1).tolist()

    def selectors(self, stage, op, flags):
        from isa_lab.full_models import HEAD_SIZES, stage_key
        return tuple(self.read(stage_key(stage, op, flags))[:len(HEAD_SIZES[stage])])

    def export(self):
        return {**super().export(), "packed_plane_bytes": self.keys.nbytes + self.values.nbytes,
                "boundary": "native phase memory adapter; full contextual SPFTransformer remains planned"}
