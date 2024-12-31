import session from 'express-session';

export const login = async (req, res) => {
    const { username, password } = req.body;

    const response = await fetch("http://127.0.0.1:5000/editor/login", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password })
    });
    
    
    if (!response.ok) {
        throw new Error("Failed to authorize user");
    }
    const data = await response.json();
    const authorized = data.authorized;
    console.log(authorized);

    if (authorized) {
        req.session.user = username;
        res.status(200).json({ message: 'Login successful', redirect: '/editor_scenario_page.html' });
    } else {
        res.status(401).json({ message: 'Invalid username or password' });
    }
}

export const logout = async (req, res) => {
    req.session.destroy(err => {
        if (err) {
            return res.status(500).json({ message: 'Logout failed' });
        }
        res.status(200).json({ message: 'Logout successful' });
    });
}

export const isAuthenticated = (req, res, next) => {
    if (req.session.user) {
        next();
    } else {
        res.redirect('/unauthorized.html');
    }
}

export const isNotAuthenticated = (req, res, next) => {
    if (req.session.user) {
      res.redirect('/editor_scenario_page.html');
    } else {
      next();
    }
  };