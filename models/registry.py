def echo_inference(data):
    return {
        "message": "Inference executed successfully",
        "input": data
    }


def uppercase_inference(data):
    return str(data).upper()


AI_FUNCTIONS = {
    "echo": echo_inference,
    "uppercase": uppercase_inference,
}

