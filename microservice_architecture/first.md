flowchart LR
  subgraph PLC Layer
    PLC["Omron PLC"]
  end

  subgraph Connector Layer
    OPCUA["OPC UA Connector\n(Go + opcua-sdk)"]
  end

  subgraph Messaging Layer
    gRPC["gRPC Broker\n(protobufs)"]
    RedisCache["Redis Cache"]
  end

  subgraph Ingestion & Storage
    Ingest["Data IngestionSvc\n(Go + gRPC)"]
    Transform["Transform & Validation\n(Go)"]
    DB["Time-Series DB\n(PostgreSQL / InfluxDB)"]
  end

  subgraph API Layer
    GraphQLGW["GraphQL Gateway\n(Node.js / Go)"]
    Clients["Clients / Dashboards"]
  end

  PLC -->|OPC UA Read| OPCUA
  OPCUA -->|Stream via gRPC| gRPC
  gRPC --> Ingest
  Ingest --> Transform
  Transform --> DB
  Transform --> RedisCache
  DB -->|Persisted Data| GraphQLGW
  RedisCache -->|Hot Reads| GraphQLGW
  GraphQLGW --> Clients
