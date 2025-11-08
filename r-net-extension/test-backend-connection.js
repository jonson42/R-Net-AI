/**
 * Simple Node.js script to test the backend connection
 * similar to how the extension would do it
 */
const axios = require('axios');

const BACKEND_URL = 'http://127.0.0.1:8000';

async function testBackendConnection() {
    console.log('🧪 Testing Backend Connection...\n');
    
    try {
        // Test 1: Health endpoint
        console.log('1️⃣ Testing health endpoint...');
        const healthResponse = await axios.get(`${BACKEND_URL}/health`, {
            timeout: 10000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        console.log(`   ✅ Status: ${healthResponse.status}`);
        console.log(`   ✅ Response:`, healthResponse.data);
        
        // Test 2: Root endpoint
        console.log('\n2️⃣ Testing root endpoint...');
        const rootResponse = await axios.get(`${BACKEND_URL}/`, {
            timeout: 10000
        });
        
        console.log(`   ✅ Status: ${rootResponse.status}`);
        console.log(`   ✅ Response:`, rootResponse.data);
        
        // Test 3: Generate endpoint with minimal data
        console.log('\n3️⃣ Testing generate endpoint...');
        const testRequest = {
            image_data: 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==',
            description: 'Create a simple hello world React component',
            tech_stack: {
                frontend: 'React',
                backend: 'FastAPI',
                database: 'PostgreSQL'
            },
            project_name: 'test-project'
        };
        
        const generateResponse = await axios.post(`${BACKEND_URL}/generate`, testRequest, {
            timeout: 30000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        console.log(`   ✅ Status: ${generateResponse.status}`);
        console.log(`   ✅ Success: ${generateResponse.data.success}`);
        console.log(`   ✅ Files generated: ${generateResponse.data.files?.length || 0}`);
        
        console.log('\n🎉 All tests passed! Backend is working correctly.');
        
    } catch (error) {
        console.error('\n❌ Backend connection failed:');
        
        if (error.code === 'ECONNREFUSED') {
            console.error('   🔴 Connection refused - Backend is not running');
            console.error('   💡 Start backend: cd r-net-backend && python3 main.py');
        } else if (error.code === 'ENOTFOUND') {
            console.error('   🔴 Host not found - Check backend URL');
        } else if (error.response) {
            console.error(`   🔴 HTTP Error: ${error.response.status}`);
            console.error(`   🔴 Response:`, error.response.data);
        } else {
            console.error(`   🔴 Error: ${error.message}`);
        }
        
        process.exit(1);
    }
}

// Run the test
testBackendConnection();