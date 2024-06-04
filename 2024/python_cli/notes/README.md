### Usage Examples

- **Create a note**:
  ```sh
    notes create "Meeting Notes" --content "Discuss project timeline and deliverables." --tags "work,meeting"
  ```

- **Read a note**:
  ```sh
    notes read "Meeting Notes"
  ```

- **Update a note**:
  ```sh
    notes update "Meeting Notes" --content "Updated content." --tags "work,updated"
  ```

- **Delete a note**:
  ```sh
    notes delete "Meeting Notes"
  ```

- **List notes**:
  ```sh
    notes show
  ```

- **List notes filtered by tag**:
  ```sh
    notes show --tag "work"
  ```

- **List notes containing a keyword**:
  ```sh
    notes show --keyword "timeline"
  ```

- **Sync notes with a remote server**:
  ```sh
    notes sync http://example.com/notes_sync
  ```