# #!/usr/bin/env python3
# """
# Test script for the Kings Queens Voting Website
# This script tests the database connection and voting functionality
# """

# import mysql.connector
# import requests
# import json

# # Database connection details
# DB_CONFIG = {
#     "host": "mysql-3f32765c-votingwebsite.i.aivencloud.com",
#     "port": 19840,
#     "user": "avnadmin",
#     "password": "AVNS_2VYcX4ttrhl8a9i8mP5",
#     "database": "votingdb",
#     "ssl_ca": "ca.pem"
# }

# def test_database_connection():
#     """Test database connection"""
#     try:
#         conn = mysql.connector.connect(**DB_CONFIG)
#         cursor = conn.cursor()
        
#         # Test basic connection
#         cursor.execute("SELECT 1")
#         result = cursor.fetchone()
#         print("✅ Database connection successful!")
        
#         # Check if tables exist
#         cursor.execute("SHOW TABLES")
#         tables = cursor.fetchall()
#         print(f"📊 Found tables: {[table[0] for table in tables]}")
        
#         # Check kings table
#         cursor.execute("SELECT COUNT(*) FROM kings")
#         king_count = cursor.fetchone()[0]
#         print(f"👑 Kings in database: {king_count}")
        
#         # Check queens table
#         cursor.execute("SELECT COUNT(*) FROM queens")
#         queen_count = cursor.fetchone()[0]
#         print(f"👸 Queens in database: {queen_count}")
        
#         cursor.close()
#         conn.close()
#         return True
        
#     except Exception as e:
#         print(f"❌ Database connection failed: {e}")
#         return False

# def test_voting_endpoint():
#     """Test the voting endpoint"""
#     try:
#         # Test vote endpoint
#         vote_data = {
#             'candidate_id': '1',
#             'candidate_type': 'king'
#         }
        
#         response = requests.post('http://localhost:5000/vote', data=vote_data)
        
#         if response.status_code == 200:
#             result = response.json()
#             if result.get('success'):
#                 print("✅ Voting endpoint working!")
#                 return True
#             else:
#                 print(f"❌ Voting failed: {result.get('message')}")
#                 return False
#         else:
#             print(f"❌ HTTP Error: {response.status_code}")
#             return False
            
#     except requests.exceptions.ConnectionError:
#         print("❌ Flask app not running. Please start the app first.")
#         return False
#     except Exception as e:
#         print(f"❌ Voting test failed: {e}")
#         return False

# def main():
#     """Run all tests"""
#     print("🧪 Testing Kings Queens Voting Website")
#     print("=" * 50)
    
#     # Test database connection
#     print("\n1. Testing Database Connection...")
#     db_ok = test_database_connection()
    
#     # Test voting endpoint
#     print("\n2. Testing Voting Endpoint...")
#     vote_ok = test_voting_endpoint()
    
#     # Summary
#     print("\n" + "=" * 50)
#     print("📋 Test Summary:")
#     print(f"   Database Connection: {'✅ PASS' if db_ok else '❌ FAIL'}")
#     print(f"   Voting Endpoint: {'✅ PASS' if vote_ok else '❌ FAIL'}")
    
#     if db_ok and vote_ok:
#         print("\n🎉 All tests passed! Your voting system is ready!")
#     else:
#         print("\n⚠️  Some tests failed. Please check the issues above.")

# if __name__ == "__main__":
#     main()
