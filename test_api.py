import requests

def test_api_health():
    """Test if the API server is running and responding"""
    
    # API endpoint
    base_url = 'http://localhost:5000'
    
    try:
        # Test the home endpoint
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ API is running and responding")
            print("Server Status: OK")
            print("You can now use the web interface at: http://localhost:5000")
        else:
            print("❌ API is running but returned unexpected status code:", response.status_code)
    
    except requests.ConnectionError:
        print("❌ Could not connect to the API server")
        print("Make sure the Flask server is running (python app.py)")
    except Exception as e:
        print(f"❌ Error occurred while testing API: {str(e)}")

if __name__ == "__main__":
    print("\nTesting API Connection...")
    test_api_health()
