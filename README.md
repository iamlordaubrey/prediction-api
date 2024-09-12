# Prediction API - Backend Task
This project is a simple **Prediction API** that allows users to:
- Register
- Log in
- Add a model
- Use their own prediction models

Each user can add multiple models. Models take in input parameters 
(floats), and generates a single output parameter (also a float).
Each user can only access their own models.

## Features:
- User registration and authentication using **username** and **password**
- JWT-based authentication for API access
- Add model to user, view all available models, and use models for
predictions
- Supports dynamic loading of models with user-specific parameters
- Uses **SQLite** with **SQLAlchemy** for database interactions
- Simple **model functions** like weighted sum and weighted average
- API documentation is available via **Swagger**

## Documentation:
- [API Documentation](http://localhost:5001)

## Running the Project
### Setup
To set up the project, run:
```commandline
make setup
make run
```

### To run tests
```commandline
make runtests
```