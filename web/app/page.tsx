import Link from 'next/link';
import { cn } from '@/lib/utils';

const features = [
  {
    title: 'Multi-Broker Support',
    description: 'Connect Zerodha, Upstox, and FYERS accounts seamlessly.',
    icon: '🔗',
  },
  {
    title: 'Strategy Marketplace',
    description: 'Browse and apply expert-curated trading strategies.',
    icon: '📈',
  },
  {
    title: 'Real-time Signals',
    description: 'Get structured trade setups with entry, target, and stop-loss.',
    icon: '⚡',
  },
  {
    title: 'Chart Overlays',
    description: 'Visual markers directly on your trading charts.',
    icon: '📊',
  },
  {
    title: 'Position Tracking',
    description: 'Real-time position monitoring across all your accounts.',
    icon: '📍',
  },
  {
    title: 'Full Order Management',
    description: 'Place, modify, and cancel orders with precision.',
    icon: '📋',
  },
];

const brokers = [
  { name: 'Zerodha', logo: '🟢' },
  { name: 'Upstox', logo: '🔵' },
  { name: 'FYERS', logo: '🟡' },
];

const strategies = [
  { name: 'Scalping Pulse', category: 'Scalping' },
  { name: 'EMA Cross', category: 'Trend Following' },
  { name: 'Mean Reversion BB', category: 'Mean Reversion' },
  { name: 'Breakout Pro', category: 'Breakout' },
];

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background-dark">
      {/* Header */}
      <header className="border-b border-background-card bg-background-dark/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">A</span>
            </div>
            <span className="text-xl font-bold text-white">AlgoReady</span>
          </div>
          <nav className="hidden md:flex space-x-8">
            <Link href="#features" className="text-neutral-300 hover:text-white transition-colors">Features</Link>
            <Link href="#brokers" className="text-neutral-300 hover:text-white transition-colors">Brokers</Link>
            <Link href="#strategies" className="text-neutral-300 hover:text-white transition-colors">Strategies</Link>
            <Link href="/login" className="text-neutral-300 hover:text-white transition-colors">Login</Link>
          </nav>
          <div className="flex items-center space-x-4">
            <Link href="/login" className="px-4 py-2 rounded-lg bg-primary-500 hover:bg-primary-600 text-white font-medium transition-colors">
              Sign In
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main>
        <section className="py-20 lg:py-32">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
              <span className="text-white">Your Brokers.</span>
              <br />
              <span className="text-primary-400">Your Strategies.</span>
              <br />
              <span className="text-white">One Trading Workspace.</span>
            </h1>
            <p className="text-xl text-neutral-400 mb-10 max-w-3xl mx-auto">
              Connect your broker accounts, apply pre-built trading strategies, and execute trades directly on your charts. 
              Trade with structure, precision, and confidence.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
              <Link 
                href="/signup" 
                className="px-8 py-4 rounded-lg bg-primary-500 hover:bg-primary-600 text-white font-bold text-lg transition-colors"
              >
                Get Started
              </Link>
              <Link 
                href="#features" 
                className="px-8 py-4 rounded-lg bg-background-card hover:bg-neutral-800 text-neutral-200 font-medium text-lg transition-colors border border-neutral-700"
              >
                Watch Demo
              </Link>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-20 bg-background-card">
          <div className="container mx-auto px-4">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-white mb-4">Powerful Features</h2>
              <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
                Build a more structured trading workflow with professional-grade tools
              </p>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {features.map((feature, index) => (
                <div key={index} className="bg-background-dark rounded-xl p-6 border border-neutral-800 hover:border-neutral-700 transition-colors">
                  <div className="text-4xl mb-4">{feature.icon}</div>
                  <h3 className="text-xl font-bold text-white mb-2">{feature.title}</h3>
                  <p className="text-neutral-400">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Brokers Section */}
        <section id="brokers" className="py-20">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">Connect Your Accounts</h2>
            <p className="text-lg text-neutral-400 mb-12 max-w-2xl mx-auto">
              Connect multiple broker accounts and track positions across all of them.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-12">
              {brokers.map((broker) => (
                <div key={broker.name} className="flex flex-col items-center">
                  <div className="w-16 h-16 bg-background-card rounded-full flex items-center justify-center mb-2">
                    <span className="text-2xl">{broker.logo}</span>
                  </div>
                  <span className="text-neutral-300 font-medium">{broker.name}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Strategies Section */}
        <section id="strategies" className="py-20 bg-background-card">
          <div className="container mx-auto px-4">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-white mb-4">Strategy Marketplace</h2>
              <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
                Browse expert-curated strategy ideas with backtested performance
              </p>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {strategies.map((strategy) => (
                <div key={strategy.name} className="bg-background-dark rounded-xl p-4 border border-neutral-800 hover:border-primary-500 transition-colors cursor-pointer">
                  <h3 className="font-bold text-white mb-1">{strategy.name}</h3>
                  <span className="text-xs text-primary-400 font-medium">{strategy.category}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-primary-500">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">Ready to trade smarter?</h2>
            <p className="text-lg text-blue-100 mb-8 max-w-2xl mx-auto">
              Join thousands of traders who have already discovered the AlgoReady advantage.
            </p>
            <Link 
              href="/signup" 
              className="px-8 py-4 rounded-lg bg-blue-900 hover:bg-blue-800 text-white font-bold text-lg transition-colors"
            >
              Create Free Account
            </Link>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-background-dark border-t border-background-card py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-bold text-white mb-4">AlgoReady</h3>
              <p className="text-neutral-400 text-sm">
                Your Brokers. Your Strategies. One Trading Workspace.
              </p>
            </div>
            <div>
              <h4 className="font-medium text-white mb-4">Product</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/features" className="text-neutral-400 hover:text-white transition-colors">Features</Link></li>
                <li><Link href="/pricing" className="text-neutral-400 hover:text-white transition-colors">Pricing</Link></li>
                <li><Link href="/strategies" className="text-neutral-400 hover:text-white transition-colors">Marketplace</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-white mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/about" className="text-neutral-400 hover:text-white transition-colors">About</Link></li>
                <li><Link href="/blog" className="text-neutral-400 hover:text-white transition-colors">Blog</Link></li>
                <li><Link href="/contact" className="text-neutral-400 hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-white mb-4">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/terms" className="text-neutral-400 hover:text-white transition-colors">Terms</Link></li>
                <li><Link href="/privacy" className="text-neutral-400 hover:text-white transition-colors">Privacy</Link></li>
                <li><Link href="/disclaimer" className="text-neutral-400 hover:text-white transition-colors">Disclaimer</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-neutral-800 mt-12 pt-8 text-center text-sm text-neutral-500">
            © 2026 AlgoReady. All rights reserved. Not a registered broker or investment adviser.
          </div>
        </div>
      </footer>
    </div>
  );
}