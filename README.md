# HBnB

This repository contains the deliverables for the HBnB project, an AirBnB-like application built progressively across multiple parts.  
Part 1 focuses on system design, including architecture planning, class modelling, and behavioural analysis through sequence diagrams.
Part 2 implements the Business Logic and Presentation layers as a RESTful API using Flask and Flask-RESTx.

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/TheKasman/holberton-hbnb.git
cd holberton-hbnb/part2
```

### 2. Install the required packages:
```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```
flask
flask-restx
```

### 3. Run the application:

```bash
python3 run.py
```

The API will be available at `http://127.0.0.1:5000`.

---

## Testing

1. Install pytest:
```bash
pip3 install pytest
```

2. Run the tests:
```bash
pytest
```
---

## 📁 Repository Contents

### Part 1 - System Design

`/Part1/class_diagrams/`

High‑resolution versions of the class diagrams created for this stage of the project.  
These are provided separately so they can be viewed or edited in full quality.

`Technical_Document.pdf`

A compiled technical document containing:

- High‑level architecture overview
- Package diagram
- Business Logic class diagram
- Sequence diagrams for key interactions
- Explanations of design decisions and system behaviour

This document acts as the blueprint for the HBnB system and demonstrates our understanding of the architecture before implementation.

### Part 2 - RESTful API


## 🎯 Purpose

**Part 1** focuses on planning the system before writing code.  
The goal is to:

- Define the structure of the system
- Model the core entities and their relationships
- Understand how the system behaves through sequence diagrams
- Establish a clear architectural foundation for later development

**Part 2** implements that design as a working API, using the **Facade pattern** to manage communication between three layers:
- **Presentation Layer** - Flask-RESTx API endpoints (`app/api/`)
- **Business Logic Layer** - Entity models with validation (`app/models/`)
- **Persistence Layer** - In-memory repository (`app/persistence/`), to be replaced by SQLAlchemy in Part 3

---

## 👥 Authors
- Andrew Kasapidis
- Matthew Wirski
- Yongshan Liang
- Patrick Macabulos
