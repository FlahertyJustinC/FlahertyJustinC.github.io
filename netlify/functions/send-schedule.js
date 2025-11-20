const sgMail = require('@sendgrid/mail');

exports.handler = async function(event) {
  try {
    if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'Method Not Allowed' };
    const token = process.env.SENDGRID_API_KEY;
    const from = process.env.FROM_EMAIL;
    const to = process.env.TO_EMAIL || 'flaherty.147@osu.edu';
    if (!token || !from) {
      console.error('Missing SENDGRID_API_KEY or FROM_EMAIL');
      return { statusCode: 500, body: JSON.stringify({ ok: false, error: 'Server not configured. Set SENDGRID_API_KEY and FROM_EMAIL.' }) };
    }

    sgMail.setApiKey(token);

    const payload = JSON.parse(event.body || '{}');
    const name = (payload.name || 'Anonymous').slice(0, 200);
    const email = (payload.email || 'no-reply@example.com').slice(0, 200);
    const csv = payload.csv || '';

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const safeName = name.replace(/[^a-z0-9_-]/gi, '_').slice(0,40);
    const filename = `availability-${timestamp}-${safeName}.csv`;

    const attachment = Buffer.from(csv, 'utf8').toString('base64');

    const msg = {
      to,
      from,
      subject: `Availability schedule from ${name}`,
      text: `${name} (${email}) submitted an availability schedule. See attached CSV.`,
      attachments: [
        {
          content: attachment,
          filename: filename,
          type: 'text/csv',
          disposition: 'attachment'
        }
      ]
    };

    await sgMail.send(msg);
    return { statusCode: 200, body: JSON.stringify({ ok: true }) };
  } catch (err) {
    console.error('send-schedule error', err && err.toString());
    return { statusCode: 500, body: JSON.stringify({ ok: false, error: err && err.message ? err.message : String(err) }) };
  }
};
