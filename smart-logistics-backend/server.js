const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');
const fs = require('fs');
const { PythonShell } = require('python-shell');
const multer = require('multer');
const csv = require('csv-parser');
require('dotenv').config();

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Configure multer for file uploads
const upload = multer({ 
  dest: 'uploads/',
  limits: { fileSize: 10 * 1024 * 1024 } // 10MB limit
});

// Store connected clients
const connectedClients = new Set();

// Socket.IO connection handling
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  connectedClients.add(socket);

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
    connectedClients.delete(socket);
  });

  socket.on('request-real-time-data', () => {
    // Send real-time updates every 5 seconds
    const interval = setInterval(() => {
      if (connectedClients.has(socket)) {
        socket.emit('data-update', generateRealTimeData());
      } else {
        clearInterval(interval);
      }
    }, 5000);
  });
});

// Generate real-time data for demo purposes
function generateRealTimeData() {
  return {
    timestamp: new Date().toISOString(),
    kpiUpdates: {
      totalOrders: Math.floor(Math.random() * 100) + 45000,
      totalRevenue: Math.floor(Math.random() * 100000) + 89000000,
      inTransitOrders: Math.floor(Math.random() * 50) + 1200,
      alertsCount: Math.floor(Math.random() * 10) + 20
    },
    newAlerts: [
      {
        id: Date.now(),
        state: ['Tamil Nadu', 'Maharashtra', 'Kerala', 'Punjab'][Math.floor(Math.random() * 4)],
        product: ['Veshti', 'Saree', 'Dhoti', 'Salwar Kameez'][Math.floor(Math.random() * 4)],
        gap: Math.floor(Math.random() * 40) + 10,
        level: ['CRITICAL', 'WARNING', 'INFO'][Math.floor(Math.random() * 3)],
        timestamp: new Date().toISOString()
      }
    ]
  };
}

// API Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

app.get('/api/dashboard', (req, res) => {
  try {
    // Return dashboard data
    const dashboardData = {
      kpi: {
        totalOrders: { value: 45678, growth: 12.5 },
        totalRevenue: { value: 89234567, growth: 8.3 },
        inTransitOrders: { value: 1234, growth: -2.1 },
        alertsCount: { value: 23, growth: 15.7 }
      },
      ordersChart: [
        { month: 'Jan', orders: 4000, revenue: 2400 },
        { month: 'Feb', orders: 3000, revenue: 1398 },
        { month: 'Mar', orders: 2000, revenue: 9800 },
        { month: 'Apr', orders: 2780, revenue: 3908 },
        { month: 'May', orders: 1890, revenue: 4800 },
        { month: 'Jun', orders: 2390, revenue: 3800 },
        { month: 'Jul', orders: 3490, revenue: 4300 },
        { month: 'Aug', orders: 4200, revenue: 5100 },
        { month: 'Sep', orders: 3800, revenue: 4700 },
        { month: 'Oct', orders: 5100, revenue: 6200 },
        { month: 'Nov', orders: 4800, revenue: 5900 },
        { month: 'Dec', orders: 6200, revenue: 7500 }
      ],
      revenueChart: [
        { month: 'Jan', revenue: 4000000, growth: 5 },
        { month: 'Feb', revenue: 4200000, growth: 5 },
        { month: 'Mar', revenue: 3800000, growth: -9.5 },
        { month: 'Apr', revenue: 4500000, growth: 18.4 },
        { month: 'May', revenue: 5200000, growth: 15.6 },
        { month: 'Jun', revenue: 4800000, growth: -7.7 },
        { month: 'Jul', revenue: 5600000, growth: 16.7 },
        { month: 'Aug', revenue: 6200000, growth: 10.7 },
        { month: 'Sep', revenue: 5800000, growth: -6.5 },
        { month: 'Oct', revenue: 6800000, growth: 17.2 },
        { month: 'Nov', revenue: 7200000, growth: 5.9 },
        { month: 'Dec', revenue: 8500000, growth: 18.1 }
      ],
      distribution: [
        { name: 'Delivered', value: 65, color: '#10B981' },
        { name: 'In Transit', value: 20, color: '#3B82F6' },
        { name: 'Delayed', value: 10, color: '#F59E0B' },
        { name: 'Overstock', value: 5, color: '#06B6D4' }
      ]
    };
    
    res.json(dashboardData);
  } catch (error) {
    console.error('Dashboard API error:', error);
    res.status(500).json({ error: 'Failed to fetch dashboard data' });
  }
});

app.post('/api/analyze', upload.single('dataFile'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No data file uploaded' });
    }

    // Process CSV file
    const results = [];
    fs.createReadStream(req.file.path)
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', async () => {
        try {
          // Call Python ML script
          const mlResults = await runPythonAnalysis(results);
          
          // Clean up uploaded file
          fs.unlinkSync(req.file.path);
          
          res.json({
            success: true,
            results: mlResults,
            recordsProcessed: results.length
          });
        } catch (mlError) {
          console.error('ML Analysis error:', mlError);
          res.status(500).json({ error: 'Failed to run ML analysis' });
        }
      });
  } catch (error) {
    console.error('Analysis API error:', error);
    res.status(500).json({ error: 'Failed to analyze data' });
  }
});

app.get('/api/alerts', (req, res) => {
  try {
    const alerts = [
      {
        id: 1,
        state: 'Tamil Nadu',
        product: 'Veshti',
        gap: 34.2,
        level: 'CRITICAL',
        revenue: 1575000,
        suggestion: 'Urgent restock by 1,204 units',
        timestamp: new Date().toISOString()
      },
      {
        id: 2,
        state: 'Punjab',
        product: 'Veshti',
        gap: 3.1,
        level: 'SAFE',
        revenue: 90000,
        suggestion: 'No action needed',
        timestamp: new Date().toISOString()
      },
      {
        id: 3,
        state: 'Maharashtra',
        product: 'Salwar Kameez',
        gap: 18.5,
        level: 'WARNING',
        revenue: 2080000,
        suggestion: 'Increase stock by 800 units',
        timestamp: new Date().toISOString()
      },
      {
        id: 4,
        state: 'Kerala',
        product: 'Saree',
        gap: -25.3,
        level: 'INFO',
        revenue: 1200000,
        suggestion: 'Excess stock - consider redistribution',
        timestamp: new Date().toISOString()
      }
    ];
    
    res.json(alerts);
  } catch (error) {
    console.error('Alerts API error:', error);
    res.status(500).json({ error: 'Failed to fetch alerts' });
  }
});

app.get('/api/map', (req, res) => {
  try {
    const mapData = {
      states: [
        {
          name: 'Tamil Nadu',
          demandScore: 3.5,
          shortage: 1200,
          revenue: 15750000,
          status: 'high-demand',
          coordinates: [11.1271, 78.6569]
        },
        {
          name: 'Maharashtra',
          demandScore: 2.8,
          shortage: 800,
          revenue: 12500000,
          status: 'moderate-demand',
          coordinates: [19.0760, 72.8777]
        },
        {
          name: 'Kerala',
          demandScore: 1.2,
          shortage: -300,
          revenue: 8900000,
          status: 'balanced',
          coordinates: [10.8505, 76.2711]
        },
        {
          name: 'Punjab',
          demandScore: 0.8,
          shortage: -500,
          revenue: 6700000,
          status: 'overstock',
          coordinates: [31.1471, 75.3412]
        },
        {
          name: 'Karnataka',
          demandScore: 2.1,
          shortage: 400,
          revenue: 9800000,
          status: 'moderate-demand',
          coordinates: [15.3173, 75.7139]
        }
      ]
    };
    
    res.json(mapData);
  } catch (error) {
    console.error('Map API error:', error);
    res.status(500).json({ error: 'Failed to fetch map data' });
  }
});

// Python ML Integration
async function runPythonAnalysis(data) {
  return new Promise((resolve, reject) => {
    const options = {
      scriptPath: path.join(__dirname, '../smart-logistics-ml'),
      args: [JSON.stringify(data)]
    };

    PythonShell.run('ml_engine.py', options, (err, results) => {
      if (err) {
        console.error('Python script error:', err);
        reject(err);
        return;
      }
      
      try {
        const analysisResults = JSON.parse(results[results.length - 1]);
        resolve(analysisResults);
      } catch (parseError) {
        console.error('Python results parsing error:', parseError);
        reject(parseError);
      }
    });
  });
}

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => {
  console.log(`🚀 Smart Logistics Backend running on port ${PORT}`);
  console.log(`📊 Dashboard API: http://localhost:${PORT}/api/dashboard`);
  console.log(`🔔 Real-time Socket.IO server active`);
});
