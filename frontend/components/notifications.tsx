'use client';

import { createContext, useContext, useState, ReactNode, useCallback, useEffect } from 'react';

type NotificationType = 'success' | 'error' | 'info' | 'warning';

interface Notification {
  id: string;
  type: NotificationType;
  message: string;
  duration?: number;
}

interface NotificationContextType {
  notifications: Notification[];
  showNotification: (type: NotificationType, message: string, duration?: number) => void;
  hideNotification: (id: string) => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export function NotificationProvider({ children }: { children: ReactNode }) {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const hideNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  }, []);

  const showNotification = useCallback((type: NotificationType, message: string, duration = 5000) => {
    const id = Math.random().toString(36).substr(2, 9);
    const newNotification = { id, type, message, duration };

    setNotifications(prev => [...prev, newNotification]);

    // Auto-remove notification after duration
    setTimeout(() => {
      hideNotification(id);
    }, duration);
  }, [hideNotification]);

  return (
    <NotificationContext.Provider value={{ notifications, showNotification, hideNotification }}>
      {children}
      <div className="fixed bottom-4 right-4 z-[1000] space-y-2 w-full max-w-sm px-4">
        {notifications.map((notification) => {
          let bgColor = '';
          let borderColor = '';
          let textColor = '';
          let icon = null;

          switch (notification.type) {
            case 'success':
              bgColor = 'bg-white border border-green-200';
              borderColor = 'border-green-200';
              textColor = 'text-green-700';
              icon = (
                <div className="flex-shrink-0">
                  <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              );
              break;
            case 'error':
              bgColor = 'bg-white border border-red-200';
              borderColor = 'border-red-200';
              textColor = 'text-red-700';
              icon = (
                <div className="flex-shrink-0">
                  <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </div>
              );
              break;
            case 'warning':
              bgColor = 'bg-white border border-yellow-200';
              borderColor = 'border-yellow-200';
              textColor = 'text-yellow-700';
              icon = (
                <div className="flex-shrink-0">
                  <svg className="w-5 h-5 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
              );
              break;
            case 'info':
              bgColor = 'bg-white border border-blue-200';
              borderColor = 'border-blue-200';
              textColor = 'text-blue-700';
              icon = (
                <div className="flex-shrink-0">
                  <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              );
              break;
          }

          return (
            <div
              key={notification.id}
              className={`p-4 rounded-xl shadow-lg flex items-start justify-between animate-slide-down transition-all duration-300 max-w-sm w-full ${bgColor} ${textColor}`}
            >
              <div className="flex items-start space-x-3 flex-1">
                {icon}
                <span className="text-sm font-medium flex-1">
                  {notification.message}
                </span>
              </div>
              <button
                onClick={() => hideNotification(notification.id)}
                className="ml-4 text-gray-500 hover:text-gray-700 focus:outline-none transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          );
        })}
      </div>
    </NotificationContext.Provider>
  );
}

export function useNotification() {
  const context = useContext(NotificationContext);
  if (context === undefined) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
}