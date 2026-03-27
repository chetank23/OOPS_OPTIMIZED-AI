import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";

export default function App() {
  const [page, setPage] = useState("dashboard");
  const [data, setData] = useState(null);

  return (
    <div className="flex h-screen bg-slate-50">
      <Sidebar setPage={setPage} />

      <div className="flex-1 flex flex-col overflow-hidden">
        {page === "dashboard" && <Dashboard data={data} />}
        {page === "upload" && <Upload setData={setData} />}
      </div>
    </div>
  );
}