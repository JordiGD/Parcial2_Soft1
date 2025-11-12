// Inicialización de la base de datos MongoDB para VirtualCoffee Pedidos API
// Este script se ejecuta automáticamente cuando se crea el contenedor

// Cambiar a la base de datos virtualcoffee_pedidos
db = db.getSiblingDB('virtualcoffee_pedidos');

// Crear usuario de aplicación con permisos completos en la base de datos
db.createUser({
  user: "pedidos_user",
  pwd: "pedidos_pass",
  roles: [
    {
      role: "dbOwner",
      db: "virtualcoffee_pedidos"
    }
  ]
});

print("✅ Usuario pedidos_user creado correctamente");

// Crear colección de secuencias para el generador de IDs
db.createCollection("sequences");

// Inicializar el contador de secuencias para órdenes
db.sequences.insertOne({
  _id: "sequence",
  seq: NumberLong(1000)  // Comenzar desde 1000 para IDs más legibles
});

// Crear colección de órdenes con validación de esquema
db.createCollection("orders", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id", "items", "totalPrice", "orderDate", "status"],
      properties: {
        id: {
          bsonType: "long",
          description: "ID secuencial de la orden"
        },
        items: {
          bsonType: "array",
          minItems: 1,
          description: "Lista de items de la orden"
        },
        totalPrice: {
          bsonType: "double",
          minimum: 0,
          description: "Precio total de la orden"
        },
        orderDate: {
          bsonType: "date",
          description: "Fecha y hora de creación de la orden"
        },
        status: {
          bsonType: "string",
          enum: ["PENDING", "CONFIRMED", "PREPARING", "READY", "COMPLETED", "REJECTED", "CANCELLED"],
          description: "Estado de la orden"
        }
      }
    }
  }
});

// Crear índices para mejorar el rendimiento
db.orders.createIndex({ "id": 1 }, { unique: true });
db.orders.createIndex({ "orderDate": -1 });
db.orders.createIndex({ "status": 1 });
db.orders.createIndex({ "totalPrice": 1 });

// Insertar órdenes de ejemplo
db.orders.insertMany([
  {
    "id": NumberLong(1001),
    "items": [
      {
        "drink": { "name": "Espresso", "size": "small", "price": 2.50 },
        "size": "small",
        "quantity": 2
      }
    ],
    "totalPrice": 5.00,
    "orderDate": new Date("2025-11-10T10:00:00.000Z"),
    "status": "COMPLETED"
  },
  {
    "id": NumberLong(1002),
    "items": [
      {
        "drink": { "name": "Cappuccino", "size": "large", "price": 4.50 },
        "size": "large",
        "quantity": 1
      },
      {
        "drink": { "name": "Americano", "size": "medium", "price": 3.00 },
        "size": "medium",
        "quantity": 1
      }
    ],
    "totalPrice": 7.50,
    "orderDate": new Date("2025-11-10T11:30:00.000Z"),
    "status": "COMPLETED"
  },
  {
    "id": NumberLong(1003),
    "items": [
      {
        "drink": { "name": "Mocha", "size": "large", "price": 5.00 },
        "size": "large",
        "quantity": 1
      }
    ],
    "totalPrice": 5.00,
    "orderDate": new Date("2025-11-11T09:15:00.000Z"),
    "status": "PREPARING"
  }
]);

// Actualizar el contador de secuencias al siguiente ID disponible
db.sequences.updateOne(
  { _id: "sequence" },
  { $set: { seq: NumberLong(1004) } }
);

// Verificar la configuración
print("✅ VirtualCoffee Pedidos MongoDB Database initialized successfully!");
print("📊 Collections created: sequences, orders");
print("👤 Application user created: pedidos_user");
print("📝 Sample orders inserted: " + db.orders.countDocuments());
print("🔢 Current sequence counter: " + db.sequences.findOne({_id: "sequence"}).seq);