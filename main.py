from fastapi import FastAPI

import handlers.expression_handler

app = FastAPI()
handlers.expression_handler.create_expression_handler(app)
