"""Мутация TestPayment (Успешная оплата)"""
def mutation_successful_payment(id):
    operationName = "TestPayment"
    variables = {
        "input": {
          "id": f"{id}"
        }
      }
    query = "mutation TestPayment($input: TestPaymentInput!) {\n  testPayment(input: $input) {" \
            "\n    ... on TestPaymentSuccess {\n      order {\n        id\n        status\n        __typename\n      }" \
            "\n      __typename\n    }\n    ... on OrderNotFoundError {\n      errorMessage\n      __typename\n    }" \
            "\n    __typename\n  }\n}\n"

    return {
        "operationName": operationName,
        "variables": variables,
        "query": query
    }


"""Мутация TestCancelOrder (Отмена)"""
def mutation_cancel(id):
    operationName = "TestCancelOrder"
    variables = {
        "input": {
          "id": f"{id}"
        }
      }
    query = "mutation TestCancelOrder($input: CancelOrderInput!) {\n  testCancelOrder(input: $input) " \
            "{\n    ... on CancelOrderSuccess {\n      order {\n        id\n        status\n        __typename\n      }" \
            "\n      __typename\n    }\n    ... on OrderNotFoundError {\n      errorMessage\n      __typename\n    }" \
            "\n    ... on OrderInactiveError {\n      errorMessage\n      __typename\n    }" \
            "\n    ... on OrderPaidError {\n      errorMessage\n      __typename\n    }\n    __typename\n  }\n}\n"

    return {
        "operationName": operationName,
        "variables": variables,
        "query": query
    }


"""Мутация TestExpire (Время истекло)"""
def mutation_expired(id):
    operationName = "TestExpire"
    variables = {
        "input": {
          "id": f"{id}"
        }
      }
    query = "mutation TestExpire($input: TestExpireInput!) {\n  testExpire(input: $input) " \
            "{\n    ... on TestExpireSuccess {\n      order {\n        id\n        status\n        __typename\n      }" \
            "\n      __typename\n    }\n    ... on OrderNotFoundError {\n      errorMessage\n      __typename\n    }" \
            "\n    ... on CantExpireError {\n      errorMessage\n      __typename\n    }\n    __typename\n  }\n}\n"

    return {
        "operationName": operationName,
        "variables": variables,
        "query": query
    }