from fastapi import FastAPI

import handlers.expression_handler
import handlers.error_handlers


# simple example for bandit
import subprocess
domain = input("Enter the Domain: ")
output = subprocess.check_output(f"nslookup {domain}", shell=True, encoding='UTF-8')

app = FastAPI()
handlers.expression_handler.create_expression_handler(app)
handlers.error_handlers.create_422_handler(app)
