import { Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import ExecutiveOverviewPage from "./pages/ExecutiveOverviewPage";
import { DataPageFactory } from "./pages/DataPageFactory";
import ETLPage from "./pages/ETLPage";
import AIPage from "./pages/AIPage";
import LoginPage from "./pages/LoginPage";
import DocumentationPage from "./pages/DocumentationPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<ExecutiveOverviewPage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="sales" element={<DataPageFactory title="Sales" endpoint="/sales" />} />
        <Route path="customers" element={<DataPageFactory title="Customers" endpoint="/customers" />} />
        <Route path="products" element={<DataPageFactory title="Products" endpoint="/products" />} />
        <Route path="regions" element={<DataPageFactory title="Regions" endpoint="/regions" />} />
        <Route path="finance" element={<DataPageFactory title="Finance" endpoint="/finance" />} />
        <Route path="etl" element={<ETLPage />} />
        <Route path="quality" element={<DataPageFactory title="Data Quality" endpoint="/data-quality" />} />
        <Route path="anomalies" element={<DataPageFactory title="Anomalies" endpoint="/anomalies" />} />
        <Route path="forecast" element={<DataPageFactory title="Forecasts" endpoint="/forecasts" />} />
        <Route path="ai" element={<AIPage />} />
        <Route path="settings" element={<DocumentationPage />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Route>
    </Routes>
  );
}
