## Usage

Requirements:

- http-echo-server (npm install -g http-echo-server npx)

```
set PORT=8124 && npx http-echo-server
```

```
make run-server
```

It will use local action but connect to other service using HTTP

---

## Input

Url: `http://localhost:3000`

#### GET /

##### Response

```json
{
  "status": "ok"
}
```

#### POST /webhook

##### Request

```json
{
  "sender": "123",
  "message": "Hello"
}
```

##### Response

It will also call HTTP output to deliver response

```json
{
  "status": "success"
}
```

## Output

Url: `http://localhost:8124`

#### Request

```json
{
  "message": "Hey what can I help you?"
}
```

#### Response

....
