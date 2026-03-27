import { useState } from "react";
import { uploadInvoices } from "../services/api";

export default function Upload({ setData }) {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const send = async () => {
    if (files.length === 0) {
      alert("Please select files first");
      return;
    }

    setLoading(true);
    try {
      const fd = new FormData();
      files.forEach(f => fd.append("files", f));
      const res = await uploadInvoices(fd);
      
      if (!res) {
        throw new Error("No response from server");
      }
      
      setData(res);
      setSuccess(true);
      setFiles([]);
      setTimeout(() => setSuccess(false), 3000);
    } catch (error) {
      console.error("Upload failed:", error);
      alert(`Failed to upload invoices: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const containerStyle = {
    flex: 1,
    overflow: 'auto',
    background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)'
  };

  const headerStyle = {
    background: 'linear-gradient(to right, #2563eb, #1d4ed8)',
    color: 'white',
    padding: '40px 32px'
  };

  const contentStyle = {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '40px 32px'
  };

  const uploadAreaStyle = {
    border: '2px dashed #bfdbfe',
    borderRadius: '8px',
    padding: '40px',
    background: 'white',
    textAlign: 'center',
    cursor: 'pointer',
    transition: 'all 0.2s'
  };

  const fileListStyle = {
    marginTop: '20px',
    padding: '16px',
    background: 'white',
    borderRadius: '8px',
    border: '1px solid #e5e7eb'
  };

  const fileItemStyle = {
    padding: '12px',
    background: '#f9fafb',
    borderRadius: '6px',
    marginBottom: '8px',
    fontSize: '14px'
  };

  const buttonStyle = {
    background: '#2563eb',
    color: 'white',
    padding: '12px 24px',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
    marginRight: '10px',
    marginTop: '20px',
    transition: 'all 0.2s'
  };

  const clearButtonStyle = {
    background: 'white',
    color: '#374151',
    padding: '12px 24px',
    border: '2px solid #d1d5db',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
    marginTop: '20px',
    transition: 'all 0.2s'
  };

  const handleUploadClick = () => {
    if (files.length === 0) {
      alert("Please select files first");
    } else {
      send();
    }
  };

  return (
    <div style={containerStyle}>
      <div style={headerStyle}>
        <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>Upload Invoices</h1>
        <p style={{ opacity: 0.9 }}>Select or drag files to process</p>
      </div>

      <div style={contentStyle}>
        <label style={{ display: 'block', cursor: 'pointer' }}>
          <div style={uploadAreaStyle}
            onDragOver={(e) => {
              e.preventDefault();
              e.currentTarget.style.background = '#eff6ff';
              e.currentTarget.style.borderColor = '#60a5fa';
            }}
            onDragLeave={(e) => {
              e.currentTarget.style.background = 'white';
              e.currentTarget.style.borderColor = '#bfdbfe';
            }}
          >
            <input
              type="file"
              multiple
              accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
              onChange={(e) => setFiles([...e.target.files])}
              style={{ display: 'none' }}
            />
            <div style={{ fontSize: '32px', marginBottom: '12px' }}>📤</div>
            <p style={{ fontSize: '16px', fontWeight: '600', color: '#1f2937', marginBottom: '8px' }}>
              Drag files here or click to browse
            </p>
            <p style={{ fontSize: '13px', color: '#6b7280' }}>
              Support: PDF, JPG, PNG, DOC, DOCX
            </p>
          </div>
        </label>

        {files.length > 0 && (
          <div style={fileListStyle}>
            <p style={{ fontWeight: '600', marginBottom: '12px', color: '#1f2937' }}>
              Selected Files ({files.length})
            </p>
            {Array.from(files).map((file, idx) => (
              <div key={idx} style={fileItemStyle}>
                📄 {file.name} - {(file.size / 1024 / 1024).toFixed(2)} MB
              </div>
            ))}
          </div>
        )}

        <div>
          <button
            onClick={handleUploadClick}
            disabled={loading}
            style={{
              ...buttonStyle,
              opacity: loading ? 0.6 : 1,
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
            onMouseEnter={(e) => !loading && (e.target.style.background = '#1d4ed8')}
            onMouseLeave={(e) => !loading && (e.target.style.background = '#2563eb')}
          >
            {loading ? 'Processing...' : 'Upload & Process'}
          </button>

          {files.length > 0 && !loading && (
            <button
              onClick={() => setFiles([])}
              style={clearButtonStyle}
              onMouseEnter={(e) => (e.target.style.background = '#f3f4f6')}
              onMouseLeave={(e) => (e.target.style.background = 'white')}
            >
              Clear
            </button>
          )}
        </div>

        {success && (
          <div style={{
            marginTop: '20px',
            padding: '16px',
            background: '#dcfce7',
            border: '1px solid #86efac',
            borderRadius: '6px',
            color: '#15803d'
          }}>
            ✓ Invoices processed successfully!
          </div>
        )}
      </div>
    </div>
  );
}