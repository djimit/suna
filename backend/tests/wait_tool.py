import asyncio

from agentpress.tool import Tool, ToolResult, openapi_schema, xml_schema


class WaitTool(Tool):
    """Test-only tool for exercising sequential and parallel execution."""

    @xml_schema(
        tag_name="wait",
        mappings=[
            {"param_name": "seconds", "node_type": "attribute", "path": "."},
            {"param_name": "message", "node_type": "content", "path": "."},
        ],
    )
    @openapi_schema({
        "type": "function",
        "function": {
            "name": "wait",
            "description": "Wait for a specified number of seconds",
            "parameters": {
                "type": "object",
                "properties": {
                    "seconds": {"type": "number"},
                    "message": {"type": "string"},
                },
                "required": ["seconds"],
            },
        },
    })
    async def wait(self, seconds: float, message: str = "") -> ToolResult:
        await asyncio.sleep(min(float(seconds), 0.05))
        return self.success_response(message or f"Waited for {seconds} seconds")

    @xml_schema(
        tag_name="wait-sequence",
        mappings=[
            {"param_name": "count", "node_type": "attribute", "path": "."},
            {"param_name": "seconds", "node_type": "attribute", "path": "."},
            {"param_name": "label", "node_type": "attribute", "path": "."},
        ],
    )
    async def wait_sequence(self, count: int, seconds: float, label: str = "Sequence") -> ToolResult:
        for _ in range(int(count)):
            await asyncio.sleep(min(float(seconds), 0.05))
        return self.success_response(label)
