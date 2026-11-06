from echo_lite.tools import calc, word_count, ToolError, REGISTRY
from echo_lite.agent import run

def test_calc_basic():
    assert calc("2+3*4") == "14"
    assert calc("10/4") == "2.5"
    print(" test_calc_basic passed")

def test_calc_errors():
    try:
        calc("1/0")
        assert False, "Expected ToolError for 1/0"
    except ToolError:
        pass

    try:
        calc("invalid_code")
        assert False, "Expected ToolError for invalid_code"
    except ToolError:
        pass
    print(" test_calc_errors passed")

def test_word_count():
    test_cases = [
        ("سلام دنیا", "2"),
        ("hello world python", "3"),
        ("", "0")
    ]
    for text, expected in test_cases:
        assert word_count(text) == expected
    print(" test_word_count passed")

def test_agent_run():
    res = run("what is 12*7 and the time in UTC?")
    assert "84" in res
    print(" test_agent_run passed")

if __name__ == "__main__":
    print("Running tests...")
    test_calc_basic()
    test_calc_errors()
    test_word_count()
    test_agent_run()
    print("\nAll tests passed successfully!")

