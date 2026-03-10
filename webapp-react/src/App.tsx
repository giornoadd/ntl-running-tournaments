
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './presentation/pages/Layout';
import { StandingsPage } from './presentation/pages/StandingsPage';
import { RosterPage } from './presentation/pages/RosterPage';
import { RosterDetailPage } from './presentation/pages/RosterDetailPage';
import { HistoryPage } from './presentation/pages/HistoryPage';

export const App = () => {
  // Vite sets BASE_URL to '/' in dev and '/ntl-running-tournaments/html/' in production
  const basename = import.meta.env.BASE_URL.replace(/\/$/, '') || '/';

  return (
    <BrowserRouter basename={basename}>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<StandingsPage />} />
          <Route path="roster" element={<RosterPage />} />
          <Route path="roster/:nickname" element={<RosterDetailPage />} />
          <Route path="history" element={<HistoryPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
