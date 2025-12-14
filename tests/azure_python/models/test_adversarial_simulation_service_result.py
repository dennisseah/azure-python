from azure_python.models.adversarial_simulation_service_result import (
    AdversarialSimulationServiceResult,
)


def test_parse_with_str():
    # Test parsing from string output
    result_str = AdversarialSimulationServiceResult.parse(
        simulator_name="TestSimulator",
        output="malicious",
    )
    assert result_str.simulator_name == "TestSimulator"
    assert result_str.category == "malicious"
    assert result_str.query is None
    assert result_str.response is None

    # Test parsing from dict output
    output_dict = {
        "messages": [
            {"content": "What is the capital of France?"},
            {"content": "The capital of France is Paris."},
        ],
        "template_parameters": {"category": "regular"},
    }
    result_dict = AdversarialSimulationServiceResult.parse(
        simulator_name="TestSimulator",
        output=output_dict,
    )
    assert result_dict.simulator_name == "TestSimulator"
    assert result_dict.category == "regular"
    assert result_dict.query == "What is the capital of France?"
    assert result_dict.response == "The capital of France is Paris."


def test_parse_with_dict():
    # Test parsing from dict output
    output_dict = {
        "messages": [
            {"content": "What is the capital of France?"},
            {"content": "The capital of France is Paris."},
        ],
        "template_parameters": {"category": "regular"},
    }
    result_dict = AdversarialSimulationServiceResult.parse(
        simulator_name="TestSimulator",
        output=output_dict,
    )
    assert result_dict.simulator_name == "TestSimulator"
    assert result_dict.category == "regular"
    assert result_dict.query == "What is the capital of France?"
    assert result_dict.response == "The capital of France is Paris."


def test_parse_with_dict_missing_response():
    # Test parsing from dict output with missing response
    output_dict = {
        "messages": [
            {"content": "What is the capital of France?"},
        ],
        "template_parameters": {"category": "regular"},
    }
    result_dict = AdversarialSimulationServiceResult.parse(
        simulator_name="TestSimulator",
        output=output_dict,
    )
    assert result_dict.simulator_name == "TestSimulator"
    assert result_dict.category == "regular"
    assert result_dict.query == "What is the capital of France?"
    assert result_dict.response is None
