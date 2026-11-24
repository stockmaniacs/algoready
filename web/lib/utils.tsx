/** Utility functions for AlgoReady */

import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge class names utility
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Format currency for Indian Rupees
 */
export function formatCurrency(amount: number, currency = 'INR'): string {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

/**
 * Format percentage
 */
export function formatPercent(value: number, decimals = 2): string {
  const sign = value >= 0 ? '+' : '';
  return `${sign}${value.toFixed(decimals)}%`;
}

/**
 * Calculate P&L color based on value
 */
export function getPnlColor(value: number): string {
  if (value > 0) return 'text-profit-500';
  if (value < 0) return 'text-loss-500';
  return 'text-neutral-400';
}

/**
 * Darken a hex color
 */
export function darkenColor(color: string, percentage: number): string {
  const num = parseInt(color.replace('#', ''), 16);
  const amt = Math.round(2.55 * percentage);
  const r = (num >> 16) - amt;
  const g = (num >> 8 & 0x00FF) - amt;
  const b = (num & 0x0000FF) - amt;
  return '#' + (0x1000000 + (r < 255 ? (r < 1 ? 0 : r) : 255) * 0x10000 + 
    (g < 255 ? (g < 1 ? 0 : g) : 255) * 0x100 + 
    (b < 255 ? (b < 1 ? 0 : b) : 255)).toString(16).slice(1);
}

/**
 * Truncate string with ellipsis
 */
export function truncate(str: string, maxLength: number): string {
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength - 3) + '...';
}

/**
 * Debounce function
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

/**
 * Format time ago
 */
export function timeAgo(date: Date | string): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - dateObj.getTime()) / 1000);
  
  if (diffInSeconds < 60) {
    return 'just now';
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  } else {
    const days = Math.floor(diffInSeconds / 86400);
    return `${days} day${days > 1 ? 's' : ''} ago`;
  }
}

/**
 * Check if value is a valid number
 */
export function isValidNumber(value: any): boolean {
  return typeof value === 'number' && !isNaN(value) && isFinite(value);
}

/**
 * Calculate percentage change
 */
export function percentChange(oldValue: number, newValue: number): number {
  if (oldValue === 0) return newValue === 0 ? 0 : Infinity;
  return ((newValue - oldValue) / oldValue) * 100;
}