import { db } from '../firebase/config';
import { collection, doc, setDoc, getDoc, onSnapshot, query, orderBy, limit } from 'firebase/firestore';

export class RealtimeService {
  static async updateKPIData(kpiData) {
    try {
      const kpiRef = doc(db, 'kpi', 'current');
      await setDoc(kpiRef, {
        ...kpiData,
        lastUpdated: new Date().toISOString()
      });
    } catch (error) {
      console.error('Error updating KPI data:', error);
    }
  }

  static async addActivity(activity) {
    try {
      const activitiesRef = collection(db, 'activities');
      const newActivity = {
        ...activity,
        timestamp: new Date().toISOString(),
        id: Date.now().toString()
      };
      await setDoc(doc(activitiesRef, newActivity.id), newActivity);
    } catch (error) {
      console.error('Error adding activity:', error);
    }
  }

  static subscribeToKPIUpdates(callback) {
    const kpiRef = doc(db, 'kpi', 'current');
    
    return onSnapshot(kpiRef, (docSnapshot) => {
      if (docSnapshot.exists()) {
        callback(docSnapshot.data());
      }
    }, (error) => {
      console.error('Error listening to KPI updates:', error);
    });
  }

  static subscribeToLiveActivities(callback) {
    const activitiesQuery = query(
      collection(db, 'activities'),
      orderBy('timestamp', 'desc'),
      limit(50)
    );
    
    return onSnapshot(activitiesQuery, (querySnapshot) => {
      const activities = [];
      querySnapshot.forEach((doc) => {
        activities.push(doc.data());
      });
      callback(activities);
    }, (error) => {
      console.error('Error listening to activities:', error);
    });
  }

  static async updateAlert(alertData) {
    try {
      const alertsRef = collection(db, 'alerts');
      const newAlert = {
        ...alertData,
        timestamp: new Date().toISOString(),
        id: Date.now().toString()
      };
      await setDoc(doc(alertsRef, newAlert.id), newAlert);
    } catch (error) {
      console.error('Error updating alert:', error);
    }
  }

  static subscribeToAlerts(callback) {
    const alertsQuery = query(
      collection(db, 'alerts'),
      orderBy('timestamp', 'desc'),
      limit(20)
    );
    
    return onSnapshot(alertsQuery, (querySnapshot) => {
      const alerts = [];
      querySnapshot.forEach((doc) => {
        alerts.push(doc.data());
      });
      callback(alerts);
    }, (error) => {
      console.error('Error listening to alerts:', error);
    });
  }

  static async logSDGImpact(impactData) {
    try {
      const impactRef = collection(db, 'sdg-impact');
      const newImpact = {
        ...impactData,
        timestamp: new Date().toISOString(),
        id: Date.now().toString()
      };
      await setDoc(doc(impactRef, newImpact.id), newImpact);
    } catch (error) {
      console.error('Error logging SDG impact:', error);
    }
  }

  static subscribeToSDGImpact(callback) {
    const impactQuery = query(
      collection(db, 'sdg-impact'),
      orderBy('timestamp', 'desc'),
      limit(100)
    );
    
    return onSnapshot(impactQuery, (querySnapshot) => {
      const impacts = [];
      querySnapshot.forEach((doc) => {
        impacts.push(doc.data());
      });
      callback(impacts);
    }, (error) => {
      console.error('Error listening to SDG impact:', error);
    });
  }
}
