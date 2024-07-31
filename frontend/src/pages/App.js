import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import YoutubeToMp4Page from './pages/YoutubeToMp4Page';
import OtherPages from './pages/OtherPages'; // Example of other page imports

const App = () => (
  <Router>
    <Switch>
      <Route path="/youtube-to-mp4" component={YoutubeToMp4Page} />
      {/* Other routes */}
    </Switch>
  </Router>
);

export default App;
