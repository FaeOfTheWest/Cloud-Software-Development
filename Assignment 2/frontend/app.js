const API_URL = 'https://libraryadminpage-fkf6h6hjhhh8hvc4.westus3-01.azurewebsites.net';


// Load all users
async function loadUsers() {
  try {
    const response = await fetch(`${API_URL}/api/users`);
    const result = await response.json();

    if (result.success) {
      const usersList = document.getElementById('usersList');
      if (result.data.length === 0) {
        usersList.innerHTML = '<p class="empty">No users found</p>';
        return;
      }
      usersList.innerHTML = result.data
        .map(u => `
          <div class="data-item">
            <strong>${u.name}</strong>
            <p>ID: ${u.id}</p>
            <p>Email: ${u.email}</p>
          </div>
        `).join('');
    }
  } catch (error) {
    console.error('Error loading users:', error);
    document.getElementById('usersList').innerHTML =
      '<p class="error-text">Failed to load users</p>';
  }
}

// Load all books
async function loadBooks() {
  try {
    const response = await fetch(`${API_URL}/api/books`);
    const result = await response.json();

    if (result.success) {
      const booksList = document.getElementById('booksList');
      if (result.data.length === 0) {
        booksList.innerHTML = '<p class="empty">No books found</p>';
        return;
      }
      booksList.innerHTML = result.data
        .map(b => `
          <div class="data-item">
            <strong>${b.bookTitle}</strong>
            <p>Author: ${b.author}</p>
            <p>ID: ${b.id}</p>
            <p>Status: 
              ${b.currentHolder !== null 
                ? `<span class="status borrowed">Borrowed (User ${b.currentHolder})</span>`
                : `<span class="status available">Available</span>`}
            </p>
            ${b.borrowDate ? `<p>Borrowed: ${b.borrowDate}</p>` : ''}
            ${b.dueDate ? `<p>Due: ${b.dueDate}</p>` : ''}
          </div>
        `).join('');
    }
  } catch (error) {
    console.error('Error loading books:', error);
    document.getElementById('booksList').innerHTML =
      '<p class="error-text">Failed to load books</p>';
  }
}

// Load available books
async function loadAvailableBooks() {
  try {
    const response = await fetch(`${API_URL}/api/books/available`);
    const result = await response.json();

    if (result.success) {
      const availableList = document.getElementById('availableBooksList');
      if (result.data.length === 0) {
        availableList.innerHTML = '<p class="empty">No books available</p>';
        return;
      }
      availableList.innerHTML = result.data
        .map(b => `
          <div class="data-item">
            <strong>${b.bookTitle}</strong>
            <p>Author: ${b.author}</p>
            <p>ID: ${b.id}</p>
            <span class="status available">Available</span>
          </div>
        `).join('');
    }
  } catch (error) {
    console.error('Error loading available books:', error);
    document.getElementById('availableBooksList').innerHTML =
      '<p class="error-text">Failed to load available books</p>';
  }
}

// Add user
document.getElementById('userForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const name = document.getElementById('userName').value;
  const email = document.getElementById('userEmail').value;

  try {
    const response = await fetch(`${API_URL}/api/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email })
    });

    const result = await response.json();
    const msg = document.getElementById('userFormMsg');

    if (result.success) {
      msg.textContent = `${result.message}`;
      msg.className = 'form-message success';
      document.getElementById('userForm').reset();
      loadUsers();
    } else {
      msg.textContent = `${result.message}`;
      msg.className = 'form-message error';
    }
  } catch (error) {
    document.getElementById('userFormMsg').textContent =
      'Error adding user';
    document.getElementById('userFormMsg').className =
      'form-message error';
  }
});

// Borrow book
document.getElementById('borrowForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const bookId = parseInt(document.getElementById('borrowBookId').value);
  const userId = parseInt(document.getElementById('borrowUserId').value);
  const dueDate = document.getElementById('borrowDueDate').value;

  try {
    const response = await fetch(`${API_URL}/api/books/borrow`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bookId, userId, dueDate })
    });

    const result = await response.json();
    const msg = document.getElementById('borrowFormMsg');

    if (result.success) {
      msg.textContent = `${result.message}`;
      msg.className = 'form-message success';
      document.getElementById('borrowForm').reset();
      loadBooks();
      loadAvailableBooks();
    } else {
      msg.textContent = `${result.message}`;
      msg.className = 'form-message error';
    }
  } catch (error) {
    document.getElementById('borrowFormMsg').textContent =
      '✗ Error borrowing book';
    document.getElementById('borrowFormMsg').className =
      'form-message error';
  }
});

// Add book
document.getElementById('addBookForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const bookTitle = document.getElementById('bookTitle').value;
  const bookAuthor = document.getElementById('bookAuthor').value;

  try {
    const response = await fetch(`${API_URL}/api/books/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bookTitle, author: bookAuthor })
    });

    const result = await response.json();
    const msg = document.getElementById('addBookFormMsg');

    if (result.success) {
      msg.textContent = `${result.message}`;
      msg.className = 'form-message success';
      document.getElementById('addBookForm').reset();
      loadBooks();
      loadAvailableBooks();
    } else {
      msg.textContent = `${result.message}`;
      msg.className = 'form-message error';
    }
  } catch (error) {
    document.getElementById('addBookFormMsg').textContent =
      'Error adding book';
    document.getElementById('addBookFormMsg').className =
      'form-message error';
  }
});

// Return book
document.getElementById('returnForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const bookId = parseInt(document.getElementById('returnBookId').value);

  try {
    const response = await fetch(`${API_URL}/api/books/return`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bookId })
    });

    const result = await response.json();
    const msg = document.getElementById('returnFormMsg');

    if (result.success) {
      msg.textContent = `${result.message}`;
      msg.className = 'form-message success';
      document.getElementById('returnForm').reset();
      loadBooks();
      loadAvailableBooks();
    } else {
      msg.textContent = `${result.message}`;
      msg.className = 'form-message error';
    }
  } catch (error) {
    document.getElementById('returnFormMsg').textContent =
      'Error returning book';
    document.getElementById('returnFormMsg').className =
      'form-message error';
  }
});

// Lookup user's books
document.getElementById('lookupUserBtn').addEventListener('click', async () => {
  const userId = parseInt(document.getElementById('userIdLookup').value);

  if (!userId) {
    document.getElementById('userBooksResult').innerHTML =
      '<p class="error-text">Please enter a User ID</p>';
    return;
  }

  try {
    const response = await fetch(`${API_URL}/api/users/${userId}/books`);
    const result = await response.json();
    const resultDiv = document.getElementById('userBooksResult');

    if (result.success) {
      if (result.data.length === 0) {
        resultDiv.innerHTML =
          `<p class="empty">${result.userName} has no books</p>`;
        return;
      }
      resultDiv.innerHTML = `
        <h3 style="color: #333; margin-bottom: 15px;">Books by ${result.userName}</h3>
        ${result.data
          .map(b => `
            <div class="data-item">
              <strong>${b.bookTitle}</strong>
              <p>Author: ${b.author}</p>
              <p>ID: ${b.id}</p>
              <p>Borrowed: ${b.borrowDate}</p>
              <p>Due: ${b.dueDate}</p>
            </div>
          `).join('')}
      `;
    } else {
      resultDiv.innerHTML =
        `<p class="error-text">${result.message}</p>`;
    }
  } catch (error) {
    console.error('Error:', error);
    document.getElementById('userBooksResult').innerHTML =
      '<p class="error-text">Error loading user books</p>';
  }
});

// Reload buttons
document.getElementById('reloadUsersBtn').addEventListener('click', loadUsers);
document.getElementById('reloadBooksBtn').addEventListener('click', loadBooks);
document.getElementById('reloadAvailableBtn').addEventListener('click',
  loadAvailableBooks);

// Initial load
loadUsers();
loadBooks();
loadAvailableBooks();