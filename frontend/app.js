const API_BASE = "https://scaling-meme-wr7x44j6qvgx29r64-8000.app.github.dev";

function showStatus(message, isError = false) {
  const el = document.getElementById("status-msg");
  el.textContent = message;
  el.style.color = isError ? "crimson" : "green";
}

function switchView(viewName) {
  document.querySelectorAll(".view").forEach(v => v.style.display = "none");
  document.getElementById(`view-${viewName}`).style.display = "block";
}

document.querySelectorAll("nav button").forEach(btn => {
  btn.addEventListener("click", () => switchView(btn.dataset.view));
});

async function apiRequest(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "Request failed");
  }
  return data;
}

function renderCatalog(books) {
  const body = document.getElementById("catalog-body");
  body.innerHTML = "";
  books.forEach(book => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${book.isbn}</td>
      <td>${book.title}</td>
      <td>${book.author}</td>
      <td>${book.category}</td>
      <td>${book.available_copies}</td>
    `;
    body.appendChild(row);
  });
}

async function loadAllBooks() {
  try {
    const books = await apiRequest("/books");
    renderCatalog(books);
  } catch (err) {
    showStatus(err.message, true);
  }
}

document.getElementById("show-all-btn").addEventListener("click", loadAllBooks);

document.getElementById("search-btn").addEventListener("click", async () => {
  const field = document.getElementById("search-field").value;
  const value = document.getElementById("search-input").value.trim();
  if (!value) return;
  try {
    const books = await apiRequest(`/books/search?${field}=${encodeURIComponent(value)}`);
    renderCatalog(books);
  } catch (err) {
    showStatus(err.message, true);
  }
});

async function loadBorrowedBooks() {
  try {
    const records = await apiRequest("/borrowed");
    const body = document.getElementById("borrowed-body");
    body.innerHTML = "";
    records.forEach(r => {
      const row = document.createElement("tr");
      row.innerHTML = `<td>${r.username}</td><td>${r.book_title}</td><td>${new Date(r.borrow_date).toLocaleString()}</td>`;
      body.appendChild(row);
    });
  } catch (err) {
    showStatus(err.message, true);
  }
}

document.getElementById("borrow-btn").addEventListener("click", async () => {
  const title = document.getElementById("borrow-title").value.trim();
  const username = document.getElementById("borrow-username").value.trim();
  try {
    await apiRequest("/borrow", { method: "POST", body: JSON.stringify({ title, username }) });
    showStatus("Book borrowed successfully");
    loadBorrowedBooks();
    loadAllBooks();
  } catch (err) {
    showStatus(err.message, true);
  }
});

document.getElementById("return-btn").addEventListener("click", async () => {
  const title = document.getElementById("return-title").value.trim();
  const username = document.getElementById("return-username").value.trim();
  try {
    await apiRequest("/return", { method: "POST", body: JSON.stringify({ title, username }) });
    showStatus("Book returned successfully");
    loadBorrowedBooks();
    loadAllBooks();
  } catch (err) {
    showStatus(err.message, true);
  }
});

document.getElementById("add-book-btn").addEventListener("click", async () => {
  const payload = {
    isbn: document.getElementById("book-isbn").value.trim(),
    title: document.getElementById("book-title").value.trim(),
    author: document.getElementById("book-author").value.trim(),
    category: document.getElementById("book-category").value.trim(),
    copies: parseInt(document.getElementById("book-copies").value, 10)
  };
  try {
    await apiRequest("/books", { method: "POST", body: JSON.stringify(payload) });
    showStatus("Book added successfully");
    loadAllBooks();
  } catch (err) {
    showStatus(err.message, true);
  }
});

document.getElementById("register-user-btn").addEventListener("click", async () => {
  const payload = {
    user_id: document.getElementById("user-id").value.trim(),
    name: document.getElementById("user-name").value.trim(),
    username: document.getElementById("user-username").value.trim()
  };
  try {
    await apiRequest("/users", { method: "POST", body: JSON.stringify(payload) });
    showStatus("User registered successfully");
  } catch (err) {
    showStatus(err.message, true);
  }
});

document.getElementById("chat-send-btn").addEventListener("click", async () => {
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return;
  const log = document.getElementById("chat-log");
  log.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
  input.value = "";
  try {
    const data = await apiRequest("/chat", { method: "POST", body: JSON.stringify({ message }) });
    log.innerHTML += `<p><strong>Librarian:</strong> ${data.reply}</p>`;
  } catch (err) {
    showStatus(err.message, true);
  }
});

loadAllBooks();
loadBorrowedBooks();




