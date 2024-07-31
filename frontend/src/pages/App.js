import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import RootPage from './pages/RootPage';
import ModulePage from './pages/ModulePage';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={RootPage} />
        <Route path="/convert/:moduleId" component={ModulePage} />
      </Switch>
    </Router>
  );
}

export default App;
