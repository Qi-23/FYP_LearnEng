import session from 'express-session';

export const login = async (req, res) => {
    const { username, password } = req.body;
    if (username === 'editor' && password === '123') {
        req.session.user = username;
        res.status(200).json({ message: 'Login successful', redirect: '/editor_scenario_page.html' });
    } else {
        res.status(401).json({ message: 'Invalid credentials' });
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