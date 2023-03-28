from fastapi import FastAPI

import handlers.expression_handler
import handlers.error_handlers

app = FastAPI()
handlers.expression_handler.create_expression_handler(app)
handlers.error_handlers.create_422_handler(app)
