import pytest
from unittest.mock import MagicMock, patch
from src.interpretability.nla_stub import generate_explanation, explain_activation
from src.copilot.semantic_mapper import map_to_copilot
from src.copilot.resolver import resolve_comptext_uri
from src.copilot.graph_connector import push_to_graph
from src.models.schemas import Analyseergebnis
from src.utils.mcp_helper import mcp_bridge
from src.interpretability.scoring_stub import compute_confidence
from src.interpretability.thought_anchor_stub import extract_anchor_points
from src.telemetry.events import PipelineEvent, CompressionEvent, CopilotSyncEvent, AuditEvent

def test_telemetry_events_instantiation():
    """
    Tests instantiation and asdict of telemetry events.
    """
    event = PipelineEvent(endpoint="test", original_tokens=100, compressed_tokens=10, savings_percentage=90.0, latency_ms=50.0)
    # Check variables
    assert event.endpoint == "test"
    assert event.savings_percentage == 90.0
    
    audit = AuditEvent(action="test_action")
    assert audit.action == "test_action"

def test_graph_connector_oauth_flow():
    """
    Tests the OAuth2 flow in the graph connector (mocked).
    """
    from src.copilot.graph_connector import auth_handler
    
    # Force credentials
    auth_handler.tenant_id = "test-tenant"
    auth_handler.client_id = "test-client"
    auth_handler.client_secret = "test-secret"
    
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "access_token": "real-token",
            "expires_in": 3600
        }
        
        token = auth_handler.get_token()
        assert token == "real-token"
        assert auth_handler._token == "real-token"
        
        # Test cached token
        assert auth_handler.get_token() == "real-token"
        mock_post.assert_called_once()

def test_nla_logic_generation():
    """
    Tests if the NLA logic produces valid feature-based explanations.
    """
    context = {"confidence": 0.95, "codes": ["P0300"], "summary": "Motorfehler"}
    explanation = generate_explanation("test_id", context)
    
    assert "Feature" in explanation
    assert "Activation:" in explanation

def test_mcp_bridge_health():
    """
    Tests the MCP bridge health check.
    """
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        assert mcp_bridge.check_health() is True
        
        mock_get.side_effect = Exception("Down")
        assert mcp_bridge.check_health() is False

def test_mcp_bridge_tool_call():
    """
    Tests calling a tool via the MCP bridge.
    """
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"success": True}
        
        res = mcp_bridge.call_tool("my_tool", {"arg": 1})
        assert res["success"] is True
        
        mock_post.side_effect = Exception("Error")
        res = mcp_bridge.call_tool("my_tool", {})
        assert res["success"] is False

def test_interpretability_stubs():
    """
    Tests the remaining interpretability stubs.
    """
    conf = compute_confidence("raw", {"output": 1})
    assert conf == 0.95
    
    anchors = extract_anchor_points("trace")
    assert len(anchors) > 0
    assert "Anchor:" in anchors[0]

def test_semantic_mapper_mapping():
    """
    Tests the conversion from AnalysisResult to Copilot Schema.
    """
    mock_result = Analyseergebnis(
        eingabe_checksum="abcdef123456",
        prioritaet="P1_KRITISCH",
        zusammenfassung="Zündaussetzer erkannt",
        massnahmen=["Check Zündkerzen"],
        erkannte_fehlercodes=["P0300"],
        konfidenz=0.98,
        modell_id="gemma2:2b",
        latenz_ms=100.0,
        rohausgabe="Raw LLM JSON",
        token_original=100,
        token_komprimiert=10
    )
    
    attachment = map_to_copilot(mock_result)
    
    assert attachment.title == "Zündaussetzer erkannt"
    assert attachment.confidence == 0.98
    assert "Feature" in attachment.explanation
    assert attachment.metadata["uri"] == "comptext://diagnostics/abcdef12"

def test_comptext_uri_resolver():
    """
    Tests the custom protocol resolver.
    """
    uri = "comptext://diagnostics/abc12345"
    resolved = resolve_comptext_uri(uri)
    
    assert resolved["resolved"] is True
    assert resolved["type"] == "diagnostics"
    assert resolved["id"] == "abc12345"

def test_graph_connector_simulation():
    """
    Tests the graph connector in simulation mode.
    """
    data = {"title": "Test Push", "content": "Sample content"}
    success = push_to_graph(data)
    assert success is True
