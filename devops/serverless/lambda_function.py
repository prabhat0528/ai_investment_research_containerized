"""
AWS Lambda Serverless Function: AI Investment Valuation & Fast Ticker Auditor
Part of Practical Module #10: Serverless Architecture with AWS Lambda & CloudWatch
"""
import json
import logging
import os
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def calculate_dcf_estimate(eps: float, growth_rate: float, discount_rate: float = 0.10, terminal_multiple: float = 15.0) -> float:
    """
    Simplified 5-year Discounted Cash Flow (DCF) model for serverless estimation.
    """
    present_value = 0.0
    current_eps = eps
    
    for year in range(1, 6):
        current_eps *= (1.0 + growth_rate)
        discount_factor = (1.0 + discount_rate) ** year
        present_value += current_eps / discount_factor
        
    terminal_value = (current_eps * terminal_multiple) / ((1.0 + discount_rate) ** 5)
    return round(present_value + terminal_value, 2)

def lambda_handler(event, context):
    """
    Main Lambda handler triggered via Amazon API Gateway proxy integration or CloudWatch Events.
    """
    start_time = time.time()
    logger.info("Received event: %s", json.dumps(event))

    # Parse request payload (supports API Gateway proxy or direct invocation)
    body = {}
    if "body" in event and event["body"]:
        try:
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
        except Exception as e:
            logger.error("Failed to parse JSON body: %s", str(e))
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Invalid JSON payload in request body"})
            }
    elif "queryStringParameters" in event and event["queryStringParameters"]:
        body = event["queryStringParameters"]
    else:
        body = event

    ticker = body.get("ticker", "AAPL").upper()
    eps = float(body.get("eps", 6.50))
    growth_rate = float(body.get("growth_rate", 0.08))
    current_price = float(body.get("price", 185.0))

    logger.info(f"Auditing Ticker: {ticker} | EPS: {eps} | Growth: {growth_rate} | Price: {current_price}")

    # Compute Fair Value and Investment Signal
    intrinsic_value = calculate_dcf_estimate(eps, growth_rate)
    upside_downside_pct = round(((intrinsic_value - current_price) / current_price) * 100, 2)
    
    if upside_downside_pct >= 15.0:
        recommendation = "BUY"
    elif upside_downside_pct <= -10.0:
        recommendation = "SELL"
    else:
        recommendation = "HOLD"

    execution_duration_ms = round((time.time() - start_time) * 1000, 2)

    result_payload = {
        "ticker": ticker,
        "current_price": current_price,
        "intrinsic_value_dcf": intrinsic_value,
        "margin_of_safety_pct": upside_downside_pct,
        "serverless_recommendation": recommendation,
        "execution_duration_ms": execution_duration_ms,
        "lambda_request_id": context.aws_request_id if hasattr(context, "aws_request_id") else "local-test-id",
        "timestamp": int(time.time())
    }

    logger.info("Audit successful: %s", json.dumps(result_payload))

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "X-Serverless-Engine": "AWS-Lambda-Python3.11"
        },
        "body": json.dumps(result_payload)
    }

if __name__ == "__main__":
    # Local verification test
    class MockContext:
        aws_request_id = "test-mock-uuid-1234"
    test_event = {"ticker": "TSLA", "eps": 3.20, "growth_rate": 0.15, "price": 220.0}
    print(json.dumps(lambda_handler(test_event, MockContext()), indent=2))
