"""Native FieldFabric readers over learned multi-axis ISA records."""
import copy
import json

from isa_lab.dependencies import field_modules
from isa_lab.full_models import StructuralSelectors


class FullFieldSelectors(StructuralSelectors):
    name = "fieldlm"
    implementation = "fieldfabric-pan-full-scope-records-v1"

    def prepare(self):
        self.api, chart = field_modules()
        self.fabric = self.api.FieldFabric()
        field = chart.RoleChartField.from_state({"charts": [], "classes": {}, "merge_log": [],
                    "role_class_merges": [], "records": [], "active_axes": None})
        self.fabric.register_view("routes", field)
        self.fabric.manage_view("routes")
        records = [chart.Record("isa", "pan-full-v1", 0, (key, json.dumps(value)),
                                f"discovery-{index}", index)
                   for index, (key, value) in enumerate(sorted(self.routes.items()))]
        self.fabric.mutate_records("routes", add=records)
        self.fabric._refresh_view_indices()
        self.program = self.api.FabricProgram("read-route", (
            self.api.ReadStep("routes", 0, {0: "$key"}, {1: "effects"}),), ("effects",))

    def read(self, key):
        # Share the immutable indexed view; query frames and materializations are disposable.
        encoded = json.dumps(key, separators=(",", ":"))
        reader = copy.copy(self.fabric)
        reader.frames = {}
        reader.abstractions = {}
        result = reader.run(self.program, {"key": encoded}, "isa", "pan-full-v1")
        if result["status"] != "resolved":
            raise ValueError(f"field route {result['status']}: {key}")
        return json.loads(result["value"])
