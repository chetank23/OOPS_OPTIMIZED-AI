export default function InvoiceTable({ data }) {
  const tableStyle = {
    width: '100%',
    marginTop: '20px',
    borderCollapse: 'collapse',
    background: 'white',
    borderRadius: '8px',
    overflow: 'hidden',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
    fontSize: '14px'
  };

  const headerStyle = {
    background: '#f3f4f6',
    padding: '12px 16px',
    textAlign: 'left',
    fontWeight: '600',
    fontSize: '13px',
    color: '#374151',
    borderBottom: '2px solid #e5e7eb'
  };

  const rowStyle = {
    padding: '16px',
    borderBottom: '1px solid #e5e7eb',
    verticalAlign: 'top'
  };

  const statusBadgeStyle = (status) => ({
    display: 'inline-block',
    padding: '4px 12px',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: '600',
    background: status === 'valid' ? '#dcfce7' : status === 'error' ? '#fee2e2' : '#fef3c7',
    color: status === 'valid' ? '#166534' : status === 'error' ? '#991b1b' : '#92400e'
  });

  const fieldBoxStyle = {
    fontSize: '13px',
    color: '#374151',
    marginBottom: '8px',
    padding: '10px 12px',
    background: '#f9fafb',
    borderRadius: '6px',
    borderLeft: '3px solid #2563eb',
    fontFamily: 'monospace'
  };

  const issueStyle = {
    fontSize: '13px',
    color: '#dc2626',
    marginBottom: '6px',
    padding: '8px 12px',
    background: '#fee2e2',
    borderRadius: '4px',
    borderLeft: '3px solid #dc2626'
  };

  if (!data || data.length === 0) {
    return (
      <div style={{
        marginTop: '20px',
        padding: '40px',
        background: 'white',
        borderRadius: '8px',
        textAlign: 'center',
        color: '#9ca3af'
      }}>
        <p>📄 No invoices processed yet</p>
      </div>
    );
  }

  return (
    <div style={{ marginTop: '20px' }}>
      <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '16px', color: '#1f2937' }}>
        Processed Invoices
      </h2>
      <table style={tableStyle}>
        <thead>
          <tr style={{ background: '#f3f4f6' }}>
            <th style={headerStyle}>File</th>
            <th style={headerStyle}>Extracted Data</th>
            <th style={headerStyle}>Status</th>
            <th style={headerStyle}>Issues</th>
          </tr>
        </thead>
        <tbody>
          {data.map((invoice, idx) => (
            <tr key={idx} style={{ background: idx % 2 === 0 ? '#fff' : '#f9fafb' }}>
              <td style={rowStyle}>📄 {invoice.filename}</td>
              <td style={rowStyle}>
                {invoice.fields && Object.keys(invoice.fields).length > 0 ? (
                  <div>
                    {invoice.fields.gstin && (
                      <div style={fieldBoxStyle}>
                        <strong>GSTIN:</strong> {invoice.fields.gstin}
                      </div>
                    )}
                    {invoice.fields.invoice_no && (
                      <div style={fieldBoxStyle}>
                        <strong>Invoice:</strong> {invoice.fields.invoice_no}
                      </div>
                    )}
                    {invoice.fields.date && (
                      <div style={fieldBoxStyle}>
                        <strong>Date:</strong> {invoice.fields.date}
                      </div>
                    )}
                    {invoice.fields.amount && (
                      <div style={fieldBoxStyle}>
                        <strong>Amount:</strong> ₹{invoice.fields.amount}
                      </div>
                    )}
                  </div>
                ) : (
                  <div style={{ color: '#9ca3af', fontSize: '13px' }}>No fields extracted</div>
                )}
              </td>
              <td style={rowStyle}>
                <span style={statusBadgeStyle(invoice.validation?.status)}>
                  {invoice.validation?.status || 'pending'}
                </span>
              </td>
              <td style={rowStyle}>
                {invoice.validation?.issues?.length > 0 ? (
                  <div>
                    {invoice.validation.issues.map((issue, i) => (
                      <div key={i} style={issueStyle}>
                        ✗ {issue}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div style={{ color: '#16a34a', fontWeight: '600' }}>✓ None</div>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}