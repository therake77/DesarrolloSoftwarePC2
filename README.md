## Desarrollo Software PC3

Nombre : Jarem Alexssander Villalobos Palomino      
Código: 20234159K
___

### Implementación 2 patrones de diseño en el proyecto

#### Patrón Singleton

La clase `SessionLocal` implementa el patrón Singleton. Es una conexión a la base de datos PostgreSQL. El método `get_db()` maneja el instanciamiento de ésta (Ver archivo `db/connection.py`):
```python
SessionLocal = sessionmaker(
   autoflush=False,
   bind=engine
)

# Función de inicialización para operaciones SQL
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Se puede implementar de manera manual un patrón singleton, pero debido al framework usado, sería implementar un singleton cuya instancia manejada es una clase Singleton. Para efectos de esta práctica, una implementación se vería así (ver `db/connection.py`) :

```python
class ExplicitDatabaseConnection:
    instance = None
    initialized = False

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if self.initialized:
            return

        SessionLocal = sessionmaker(bind=engine, autoflush=False)
        self.db = SessionLocal()

        self.initialized = True

``` 
Nota: El sistema de creación de Python es peculiar. Primero llama a `__new__` para instanciar una clase, y luego llama a `__init__` para *rellenar* sus atributos. Pero como también interceptamos la creación en `__init__`, entonces la clase si se comporta como un singleton.

#### Patrón Builder

Como mencioné en el manuscrito, una buena idea sería abstraer la construcción de un Préstamo (Loan)
usando el patrón Builder. Esto da la ventaja de implementar validación en la construcción de un préstamo, capturando errores antes que contaminen la base de datos. (Ver archivo `domain/loan.py`)
```python

class LoanBuilder:
    def __init__(self):
        self._id = None
        self._user_id = None
        self._copy_code = None
        self._aproval_date = None
        self._due_date = None
        self._retrival_date = None
        self._status = None

    def set_id(self, id: int):
        self._id = id
        return self

    def set_user_id(self, user_id: int):
        self._user_id = user_id
        return self

    def set_copy_code(self, copy_code: str):
        self._copy_code = copy_code
        return self

    def set_aproval_date(self, aproval_date: date):
        if self._due_date and aproval_date > self._due_date:
            raise ValueError("Aproval date cannot be after due date.")
        self._aproval_date = aproval_date
        return self

    def set_due_date(self, due_date: date):
        if self._aproval_date and due_date < self._aproval_date:
            raise ValueError("Due date cannot be before aproval date.")
        self._due_date = due_date
        return self

    def set_retrival_date(self, retrival_date: date):
        if self._aproval_date and retrival_date < self._aproval_date:
            raise ValueError("Retrival date cannot be before aproval date.")
        self._retrival_date = retrival_date
        return self

    def set_status(self, status: EstadoPrestamo):
        self._status = status
        return self

    def build(self) -> Loan:
        return Loan(
            id=self._id,
            user_id=self._user_id,
            copy_code=self._copy_code,
            aproval_date=self._aproval_date,
            due_date=self._due_date,
            retrival_date=self._retrival_date,
            status=self._status
        )
```

