import './app.css'

export function App() {
  const invoiceRows = [
    ['GRP-001', 'Glass desk lamp', '2', '2,400', '12%'],
    ['GRP-002', 'GST filing support', '1', '8,500', '18%'],
    ['GRP-003', 'Thermal printer paper', '6', '180', '5%'],
  ]

  const steps = [
    'Capture invoice from PDF, photo, or email.',
    'Auto-read GSTIN, HSN, tax slabs, and totals.',
    'Validate before filing or export to your ERP.',
  ]

  const metrics = [
    ['Accuracy', '99.2%'],
    ['Invoices today', '128'],
    ['Avg. review time', '14 sec'],
    ['Mismatch alerts', '03'],
  ]

  return (
    <main class="shell">
      <section class="hero-panel">
        <div class="hero-copy">
          <span class="eyebrow">GST Invoice AI</span>
          <h1>Turn messy bills into clean, filed-ready GST data.</h1>
          <p class="lead">
            Review invoices faster with document capture, GSTIN validation, tax breakdowns,
            and export-ready summaries in one workspace.
          </p>

          <div class="hero-actions">
            <a class="primary" href="#workspace">
              Scan invoice
            </a>
            <a class="secondary" href="#review">
              Open review queue
            </a>
          </div>

          <ul class="metric-grid" aria-label="Platform metrics">
            {metrics.map(([label, value]) => (
              <li>
                <strong>{value}</strong>
                <span>{label}</span>
              </li>
            ))}
          </ul>
        </div>

        <div class="hero-card" id="workspace">
          <div class="card-header">
            <span>Live workspace</span>
            <span class="status">Active</span>
          </div>

          <div class="upload-zone">
            <div class="upload-icon">⤒</div>
            <div>
              <h2>Drop invoices, receipts, or GST statements</h2>
              <p>PDF, JPG, PNG, and scanned email attachments supported.</p>
            </div>
          </div>

          <div class="scan-summary">
            <div>
              <span>Supplier</span>
              <strong>Shree Bharat Traders</strong>
            </div>
            <div>
              <span>GSTIN</span>
              <strong>27AAJCS2418Q1ZV</strong>
            </div>
            <div>
              <span>Invoice total</span>
              <strong>₹13,956.00</strong>
            </div>
            <div>
              <span>Risk score</span>
              <strong class="risk-low">Low</strong>
            </div>
          </div>

          <div class="invoice-table" id="review">
            <div class="table-head">
              <span>Item</span>
              <span>Qty</span>
              <span>Value</span>
              <span>Tax</span>
            </div>
            {invoiceRows.map(([code, item, qty, value, tax]) => (
              <div class="table-row">
                <span>
                  <strong>{code}</strong>
                  <small>{item}</small>
                </span>
                <span>{qty}</span>
                <span>₹{value}</span>
                <span>{tax}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section class="feature-grid">
        <div class="feature-card">
          <h2>What the assistant handles</h2>
          <ul>
            {steps.map((step) => (
              <li>{step}</li>
            ))}
          </ul>
        </div>

        <div class="feature-card soft">
          <h2>Validation controls</h2>
          <ul class="checks">
            <li>GSTIN format check</li>
            <li>Tax slab consistency check</li>
            <li>Duplicate invoice detection</li>
            <li>Mismatch alerts before filing</li>
          </ul>
        </div>

        <div class="feature-card callout">
          <h2>Ready for ERP export</h2>
          <p>
            Push clean invoice data into accounting workflows with structured totals,
            supplier details, and item-level tax values.
          </p>
          <a class="inline-link" href="#workspace">
            Preview output
          </a>
        </div>
      </section>
    </main>
  )
}
