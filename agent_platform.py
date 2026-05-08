from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="AgentNet Central Node", description="A semantic network for AI agents")

# --- Registry Models ---
class ServiceParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool

class ServiceRegistration(BaseModel):
    id: str
    name: str
    description: str
    endpoint: str
    method: str
    parameters: List[ServiceParameter]

# In-memory registry
REGISTRY: Dict[str, ServiceRegistration] = {}

# --- Core Platform Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Welcome to AgentNet V1. The web for machines. Navigate to /registry to discover services."}

@app.post("/registry/register", status_code=201)
def register_service(service: ServiceRegistration):
    REGISTRY[service.id] = service
    return {"status": "registered", "service_id": service.id}

@app.get("/registry", response_model=List[ServiceRegistration])
def list_services():
    return list(REGISTRY.values())

@app.get("/registry/search")
def search_services(query: str):
    """A naive semantic search for agents to find tools."""
    results = []
    q = query.lower()
    for srv in REGISTRY.values():
        if q in srv.name.lower() or q in srv.description.lower():
            results.append(srv)
    return results

# --- Built-in Mock Services ---

class WeatherQuery(BaseModel):
    location: str

@app.post("/services/weather")
def get_weather(query: WeatherQuery):
    # Mock weather data
    return {"location": query.location, "temperature_celsius": 22, "condition": "Sunny"}

class CalculatorQuery(BaseModel):
    expression: str

import ast
import operator

# Supported operators for our safe calculator
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg
}

def evaluate_expr(node):
    if isinstance(node, ast.Constant): # <constant> e.g., number
        return node.value
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](evaluate_expr(node.left), evaluate_expr(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](evaluate_expr(node.operand))
    else:
        raise TypeError(node)

@app.post("/services/calculator")
def calculate(query: CalculatorQuery):
    try:
        result = evaluate_expr(ast.parse(query.expression, mode='eval').body)
        return {"expression": query.expression, "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Auto-register built-in services on startup
@app.on_event("startup")
def startup_event():
    weather_srv = ServiceRegistration(
        id="core.weather.v1",
        name="WeatherService",
        description="Provides current weather conditions for a given location.",
        endpoint="/services/weather",
        method="POST",
        parameters=[ServiceParameter(name="location", type="string", description="City name", required=True)]
    )
    REGISTRY[weather_srv.id] = weather_srv

    calc_srv = ServiceRegistration(
        id="core.calculator.v1",
        name="MathCalculator",
        description="Evaluates simple mathematical expressions.",
        endpoint="/services/calculator",
        method="POST",
        parameters=[ServiceParameter(name="expression", type="string", description="Math expression like '2+2'", required=True)]
    )
    REGISTRY[calc_srv.id] = calc_srv
