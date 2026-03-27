import StatCard from "../components/Statcard";
import InvoiceTable from "../components/InvoiceTable";

export default function Dashboard({ data }) {
  const containerStyle = {
    flex: 1,
    overflow: 'auto',
    background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)'
  };

  const headerStyle = {
    background: 'linear-gradient(to right, #2563eb, #1d4ed8)',
    color: 'white',
    padding: '40px 32px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
  };

  const contentStyle = {
    maxWidth: '1280px',
    margin: '0 auto',
    padding: '32px'
  };

  const gridStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
    marginBottom: '32px'
  };

  const summaryStyle = {
    background: 'white',
    padding: '20px',
    borderRadius: '8px',
    marginBottom: '32px',
    borderLeft: '4px solid #2563eb',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)'
  };

  const processedCount = data?.processed?.length || 0;
  const matchedCount = data?.reconciliation?.matched?.length || 0;
  const mismatchedCount = data?.reconciliation?.mismatched?.length || 0;

  return (
    <div style={containerStyle}>
      <div style={headerStyle}>
        <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>Dashboard</h1>
        <p style={{ opacity: 0.9 }}>Monitor and manage your invoice processing</p>
      </div>

      <div style={contentStyle}>
        <div style={gridStyle}>
          <StatCard title="Total Invoices" value={processedCount} />
          <StatCard title="Matched Records" value={matchedCount} />
          <StatCard title="Issues Found" value={mismatchedCount} />
        </div>

        {processedCount > 0 && (
          <div style={summaryStyle}>
            <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '8px', color: '#1f2937' }}>
              Summary
            </h3>
            <p style={{ color: '#6b7280', fontSize: '14px' }}>
              Processed <span style={{ fontWeight: 'bold', color: '#2563eb' }}>{processedCount}</span> invoices with{' '}
              <span style={{ fontWeight: 'bold', color: '#16a34a' }}>{matchedCount}</span> successful matches and{' '}
              <span style={{ fontWeight: 'bold', color: '#dc2626' }}>{mismatchedCount}</span> requiring review.
            </p>
          </div>
        )}

        <InvoiceTable data={data?.processed} />
      </div>
    </div>
  );
}