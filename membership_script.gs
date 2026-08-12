function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const data = JSON.parse(e.postData.contents);

    // Log data to Google Sheet (8 columns - removed residentialAddress)
    sheet.appendRow([
      new Date(),
      data.fullName || '',
      data.email || '',
      data.phone || '',
      data.location || '',
      data.referralSource || '',
      data.ministryInterests || 'None',
      data.aboutYou || ''
    ]);

    // Send confirmation email
    const emailSubject = "Membership Application Confirmation - Word Temple Church of God International";
    const emailBody = `Dear ${data.fullName || 'Member'},\n\n` +
      `Thank you for submitting your membership application to Word Temple Church of God International.\n\n` +
      `We have received your details and ministry preferences. Our pastoral and ministry team will connect with you soon.\n\n` +
      `Blessings,\nWord Temple Church of God International`;

    MailApp.sendEmail({
      to: data.email,
      subject: emailSubject,
      body: emailBody
    });

    return ContentService.createTextOutput(JSON.stringify({ status: "success" }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
