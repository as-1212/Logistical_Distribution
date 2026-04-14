import { useEffect, useState } from 'react'
import { io } from 'socket.io-client'

const useSocket = () => {
  const [socket, setSocket] = useState(null)
  const [connected, setConnected] = useState(false)
  const [realTimeData, setRealTimeData] = useState(null)

  useEffect(() => {
    // Initialize socket connection
    const socketInstance = io('http://localhost:5000', {
      transports: ['websocket', 'polling']
    })

    socketInstance.on('connect', () => {
      console.log('Connected to server')
      setConnected(true)
      setSocket(socketInstance)
      
      // Request real-time data
      socketInstance.emit('request-real-time-data')
    })

    socketInstance.on('disconnect', () => {
      console.log('Disconnected from server')
      setConnected(false)
    })

    socketInstance.on('data-update', (data) => {
      setRealTimeData(data)
    })

    // Cleanup on unmount
    return () => {
      if (socketInstance) {
        socketInstance.disconnect()
      }
    }
  }, [])

  const sendRealTimeRequest = () => {
    if (socket && connected) {
      socket.emit('request-real-time-data')
    }
  }

  return {
    socket,
    connected,
    realTimeData,
    sendRealTimeRequest
  }
}

export default useSocket
