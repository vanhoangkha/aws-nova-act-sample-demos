#!/usr/bin/env python3
"""
Sample 05: Handling Sensitive Information
Demo safe password and sensitive data input methods
"""

import os
import getpass
from nova_act import NovaAct, BOOL_SCHEMA

def demo_safe_password_entry():
    """Demo safe password input"""
    
    print("Demo Safe Password Input")
    print("-" * 30)
    
    try:
        with NovaAct(
            starting_page="https://example.com/login",  # Sample login page
            headless=False  # Need to see for demo
        ) as nova:
            
            # Step 1: Fill username and focus on password field
            print("Filling username...")
            nova.act("enter username 'demo_user' and click on the password field")
            
            # Step 2: Input password via Playwright (not through model)
            print("Enter password (hidden input):")
            password = getpass.getpass("Password: ")
            
            # Use Playwright API directly to input password
            print("Entering password via Playwright...")
            nova.page.keyboard.type(password)
            
            # Step 3: Continue with Nova Act
            print("Logging in...")
            nova.act("click the sign in button")
            
            # Check result
            result = nova.act("Am I successfully logged in?", schema=BOOL_SCHEMA)
            
            if result.matches_schema and result.parsed_response:
                print("Login successful!")
            else:
                print("Login failed")
                
    except Exception as e:
        print(f"Error: {e}")

def demo_captcha_handling():
    """Demo CAPTCHA handling"""
    
    print("\nDemo CAPTCHA Handling")
    print("-" * 30)
    
    try:
        with NovaAct(
            starting_page="https://example.com/captcha",
            headless=False  # Need to see to solve CAPTCHA
        ) as nova:
            
            # Check for CAPTCHA
            print("Checking for CAPTCHA...")
            result = nova.act("Is there a captcha on the screen?", schema=BOOL_SCHEMA)
            
            if result.matches_schema and result.parsed_response:
                print("CAPTCHA detected!")
                print("Please solve the CAPTCHA and press Enter when done...")
                input("Press Enter to continue...")
                
                # Continue after solving CAPTCHA
                nova.act("submit the form")
                print("Form submitted after solving CAPTCHA")
                
            else:
                print("No CAPTCHA found, continuing normally")
                nova.act("submit the form")
                
    except Exception as e:
        print(f"Error: {e}")

def demo_credit_card_entry():
    """Demo safe credit card information input"""
    
    print("\nDemo Credit Card Information Input")
    print("-" * 30)
    
    # Test card information (not real)
    test_card = {
        "number": "4111111111111111",  # Test card number
        "expiry": "12/25",
        "cvv": "123",
        "name": "Test User"
    }
    
    try:
        with NovaAct(
            starting_page="https://example.com/checkout",
            headless=False
        ) as nova:
            
            print("Filling credit card information...")
            
            # Focus on each field and use Playwright to input
            nova.act("click on the credit card number field")
            nova.page.keyboard.type(test_card["number"])
            
            nova.act("click on the expiry date field")
            nova.page.keyboard.type(test_card["expiry"])
            
            nova.act("click on the CVV field")
            nova.page.keyboard.type(test_card["cvv"])
            
            nova.act("click on the cardholder name field")
            nova.page.keyboard.type(test_card["name"])
            
            print("Credit card information filled via Playwright API")
            print("Sensitive information not sent through model")
            
            # Continue with Nova Act
            nova.act("review the payment information")
            
    except Exception as e:
        print(f"Error: {e}")

def demo_environment_variables():
    """Demo using environment variables for sensitive data"""
    
    print("\nDemo Environment Variables")
    print("-" * 30)
    
    # Get information from environment variables
    username = os.getenv('DEMO_USERNAME', 'default_user')
    api_token = os.getenv('DEMO_API_TOKEN', 'default_token')
    
    print(f"Username from env: {username}")
    print(f"API Token from env: {api_token[:8]}..." if api_token != 'default_token' else "Using default token")
    
    try:
        with NovaAct(
            starting_page="https://api.example.com/login",
            headless=True
        ) as nova:
            
            # Use Nova Act for navigation
            nova.act("find the API authentication form")
            
            # Use Playwright for sensitive data
            nova.act("click on the username field")
            nova.page.keyboard.type(username)
            
            nova.act("click on the API token field")
            nova.page.keyboard.type(api_token)
            
            nova.act("submit the authentication form")
            
            print("API authentication completed")
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Demo handling sensitive information"""
    
    # Check API key
    api_key = os.getenv('NOVA_ACT_API_KEY')
    if not api_key:
        print("Please set NOVA_ACT_API_KEY")
        return
    
    print("Sample 05: Handling Sensitive Information")
    print("=" * 50)
    print("Best practices for sensitive data")
    
    print("\nIMPORTANT NOTES:")
    print("• Never send passwords/sensitive data through act()")
    print("• Use Playwright API directly: nova.page.keyboard.type()")
    print("• Use getpass() for safe password input")
    print("• Use environment variables for credentials")
    print("• Screenshots may contain sensitive data if displayed on screen")
    
    # Demo scenarios
    demos = [
        ("Safe Password Entry", demo_safe_password_entry),
        ("CAPTCHA Handling", demo_captcha_handling),
        ("Credit Card Entry", demo_credit_card_entry),
        ("Environment Variables", demo_environment_variables)
    ]
    
    for demo_name, demo_func in demos:
        print(f"\n{'='*50}")
        print(f"{demo_name}")
        print(f"{'='*50}")
        
        try:
            demo_func()
        except KeyboardInterrupt:
            print("Demo interrupted by user")
            break
        except Exception as e:
            print(f"Error in {demo_name}: {e}")
        
        print(f"Completed {demo_name}")
    
    print(f"\nThis example demonstrates:")
    print("   • getpass.getpass() for password input")
    print("   • nova.page.keyboard.type() for sensitive data")
    print("   • CAPTCHA detection and handling")
    print("   • Environment variables for credentials")
    print("   • Security best practices")
    
    print(f"\nSecurity Checklist:")
    print("   Don't send passwords through act()")
    print("   Use Playwright API for sensitive input")
    print("   Handle CAPTCHA with user interaction")
    print("   Use environment variables")
    print("   Be careful with screenshots")

if __name__ == "__main__":
    main()
