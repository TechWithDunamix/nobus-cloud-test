from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_loan_approval_email(user_email: str, user_name: str, amount: float, tenure: int):
    """
    Send a nice HTML email to the user when their loan is approved.
    """
    subject = "🎉 Congratulations! Your Loan Application is Approved - Nobus Cloud"
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background-color: #4CAF50;
                color: white;
                text-align: center;
                padding: 20px;
            }}
            .content {{
                padding: 30px;
                line-height: 1.6;
            }}
            .details-box {{
                background-color: #f9f9f9;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 15px;
                margin: 20px 0;
            }}
            .footer {{
                background-color: #333;
                color: white;
                text-align: center;
                padding: 15px;
                font-size: 12px;
            }}
            .button {{
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 4px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Loan Approved!</h1>
            </div>
            <div class="content">
                <p>Hello <strong>{user_name}</strong>,</p>
                <p>We are thrilled to inform you that your loan application has been <strong>APPROVED</strong>!</p>
                
                <div class="details-box">
                    <p><strong>Amount:</strong> ${amount:,.2f}</p>
                    <p><strong>Tenure:</strong> {tenure} Months</p>
                    <p><strong>Status:</strong> <span style="color: #4CAF50; font-weight: bold;">ACTIVE</span></p>
                </div>
                
                <p>The funds will be disbursed to your registered account shortly. Thank you for choosing Nobus Cloud for your financial needs.</p>
                
                <a href="#" class="button">View Dashboard</a>
            </div>
            <div class="footer">
                &copy; 2026 Nobus Cloud. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
