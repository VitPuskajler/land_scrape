import smtplib
import ssl
from email.message import EmailMessage


class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        

    def table_create(self, bazos = None, reality=None, topreality=None):
        self.mail_html = ""
        # Provide sensible defaults if parameters are None or empty
        """ display_image_url = img_url if img_url else 'https://placehold.co/180x180/E0E0E0/333333?text=No+Image'
        display_description = description_text if description_text else 'No description available.'
        display_price = price_text if price_text else 'N/A' """
        self.display_image_url = None
        self.display_description = None
        self.display_price = None


        if bazos:
            for b_ad in bazos:
                self.html_template = f"""
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; font-family: 'Inter', Arial, sans-serif;">
                    <tr>
                        <td style="padding: 20px; text-align: center; color: #333333;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                <tr>
                                    <td valign="top" width="33.33%" style="padding: 10px; text-align: center;">
                                    <a href = "{b_ad["Source"]}" target="_blank" style="text-decoration: none; display: block;">
                                        <img src="{b_ad["Photo"][1]}" alt="Product Image" width="180" style="max-width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 8px;">
                                    </a>
                                    </td>

                                    <td valign="top" width="33.33%" style="padding: 10px; text-align: left; font-size: 14px; line-height: 20px; color: #555555;">
                                        <p style="margin: 0;">
                                            {b_ad["Title"]}
                                        </p>
                                    </td>

                                    <td valign="top" width="33.33%" style="padding: 10px; text-align: center;">
                                        <p style="margin: 0; font-size: 28px; font-weight: bold; color: #000000; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
                                            <span style="color: #000000;">{b_ad["Price"]}</span>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                """
                self.mail_html += self.html_template

        if reality:
            for b_ad in reality:
                self.html_template = f"""
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; font-family: 'Inter', Arial, sans-serif;">
                    <tr>
                        <td style="padding: 20px; text-align: center; color: #333333;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                <tr>
                                    <td valign="top" width="33.33%" style="padding: 10px; text-align: center;">
                                    <a href = "{b_ad["Source"]}" target="_blank" style="text-decoration: none; display: block;">
                                        <img src="{b_ad["Photo"]}" alt="Product Image" width="180" style="max-width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 8px;">
                                    </a>
                                    </td>

                                    <td valign="top" width="33.33%" style="padding: 10px; text-align: left; font-size: 14px; line-height: 20px; color: #555555;">
                                        <p style="margin: 0;">
                                            {b_ad["Title"]}
                                        </p>
                                    </td>

                                    <td valign="top" width="33.33%" style="padding: 10px; text-align: center;">
                                        <p style="margin: 0; font-size: 28px; font-weight: bold; color: #000000; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
                                            <span style="color: #000000;">{b_ad["Price"]}</span>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                """
                self.mail_html += self.html_template

        if topreality:
            for b_ad in topreality:
                self.html_template = f"""
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; font-family: 'Inter', Arial, sans-serif;">
                    <tr>
                        <td style="padding: 20px; text-align: center; color: #333333;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                <tr>
                                    <td valign="top" width="33.33%" style="padding: 10px; text-align: center;">
                                    <a href = "{b_ad["Source"]}" target="_blank" style="text-decoration: none; display: block;">
                                        <img src="{b_ad["Photo"][-1]}" alt="Product Image" width="180" style="max-width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 8px;">
                                    </a>
                                    </td>

                                    <td valign="top" width="33.33%" style="padding: 10px; text-align: left; font-size: 14px; line-height: 20px; color: #555555;">
                                        <p style="margin: 0;">
                                            {b_ad["Title"]}
                                        </p>
                                    </td>

                                    <td valign="top" width="33.33%" style="padding: 10px; text-align: center;">
                                        <p style="margin: 0; font-size: 28px; font-weight: bold; color: #000000; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
                                            <span style="color: #000000;">{b_ad["Price"]}</span>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                """
                self.mail_html += self.html_template
        
        with open("test.html", "w", encoding="utf-8") as f:
            f.write(self.mail_html)
        
        return self.mail_html

    def send_email(self, data, mail_add, mail_pass):
        msg = EmailMessage()
        msg["From"]=mail_add
        msg["To"]=mail_add
        msg["Subject"] = "Pozemky"
        msg.set_content(data, subtype="html")

        try:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=mail_add, password=mail_pass)
                connection.send_message(msg)
            print("Email was sent!")
        except Exception as e:
            print(f'Error: I was unable to send your email: {e}')