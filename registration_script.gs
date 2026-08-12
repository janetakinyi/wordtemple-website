function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const data = JSON.parse(e.postData.contents);

    sheet.appendRow([
      new Date(),
      data.fullName,
      data.organization || "N/A",
      data.email,
      data.phone,
      data.conference,
      data.accommodation,
      data.mealPreference,
      data.specialRequests || "N/A"
    ]);

    const emailSubject = "Conference Registration Confirmation - Word Temple Church of God International";
    const emailBody = `Dear ${data.fullName},\n\n` +
      `Thank you for registering for ${data.conference}.\n\n` +
      `We have received your registration details. Our team will contact you soon with further information.\n\n` +
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
