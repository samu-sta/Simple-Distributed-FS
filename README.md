# Distributed File Storage System

This project implements a distributed file storage system with a master node and storage nodes. The system allows users to create, read, update, and delete files, which are fragmented and stored across multiple storage nodes.

## Components

1. **NodoMaestro.py**: The master node that manages file metadata and coordinates file operations.
2. **NodoAlmacenamiento.py**: The storage nodes that store file fragments.
3. **Cliente.py**: The client that interacts with the master node to perform file operations.
4. **Interfaz.py**: The user interface for interacting with the client.

## How It Works

- **Master Node (NodoMaestro.py)**: 
  - Manages metadata for files.
  - Splits files into fragments and distributes them to storage nodes.
  - Coordinates file operations like create, read, update, and delete.

- **Storage Nodes (NodoAlmacenamiento.py)**:
  - Store file fragments.
  - Handle requests to save, read, and delete file fragments.

- **Client (Cliente.py)**:
  - Sends requests to the master node to perform file operations.

- **User Interface (Interfaz.py)**:
  - Provides a menu-driven interface for users to interact with the system.

## File Operations

1. **Create File**:
   - Splits the file into two fragments.
   - Sends each fragment to a different storage node.
   - Updates the metadata in the master node.

2. **Read File**:
   - Retrieves the file fragments from the storage nodes.
   - Combines the fragments to reconstruct the file.

3. **Update File**:
   - Similar to creating a file, but updates the existing file fragments.

4. **Delete File**:
   - Deletes the file fragments from the storage nodes.
   - Removes the metadata from the master node.

## Running the System

1. **Start Storage Nodes**:
  ```sh
  python3 NodoAlmacenamiento.py
  ```
  Start as many storage nodes as needed.

2. **Start Master Node**:
  ```sh
  python3 NodoMaestro.py
  ```

3. **Start Client**:
  ```sh
  python3 Cliente.py
  ```

4. **Start User Interface**:
  ```sh
  python3 Interfaz.py
  ```

## Requirements

- Python 3.x
- `socket` library for network communication
- `threading` library for handling concurrent connections

## License

This project is licensed under the MIT License.
