import { useState } from 'react';
import { Upload, Play, Loader2, LogOut, Lock, BookOpen, ExternalLink } from 'lucide-react';
import vitaLogo from '../imports/vita.png';

const API_URL = 'http://127.0.0.1:8000';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [loginError, setLoginError] = useState('');

  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [resultUrl, setResultUrl] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState('yolov3-tiny');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileSelect = (file: File) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResultUrl(null);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) handleFileSelect(file);
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoggingIn(true);
    setLoginError('');

    try {
      // Try JSON first
      let response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: email,
          password: password,
        }),
      });

      // Fallback to form-data if JSON fails
      if (response.status === 422) {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        response = await fetch(`${API_URL}/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: formData,
        });
      }

      if (response.ok) {
        const data = await response.json();
        const accessToken = data.access_token || data.token;

        setToken(accessToken);
        setIsAuthenticated(true);
        setLoginError('');
      } else {
        const errorText = await response.text();
        setLoginError(`Erro: ${response.status} - ${errorText}`);
      }
    } catch (error) {
      setLoginError(`Erro de conexão: ${error}`);
    } finally {
      setIsLoggingIn(false);
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setToken(null);
    setEmail('');
    setPassword('');
    setSelectedImage(null);
    setPreviewUrl(null);
    setResultUrl(null);
  };

  const handleRunDetection = async () => {
    if (!selectedImage) return;

    setIsProcessing(true);

    try {
      const formData = new FormData();
      formData.append('file', selectedImage);

      const response = await fetch(`${API_URL}/api/vision/detect?model=${selectedModel}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        setResultUrl(URL.createObjectURL(blob));
      } else {
        console.error('Detection failed:', response.statusText);
        alert('Erro ao processar imagem. Verifique se a API está rodando.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Erro de conexão com a API.');
    } finally {
      setIsProcessing(false);
    }
  };

  const architectureLayers = [
    {
      title: 'Connection',
      description: 'Data acquisition and IoT sensor integration',
      color: 'from-slate-500 to-slate-600'
    },
    {
      title: 'Conversion',
      description: 'Data processing and transformation',
      color: 'from-red-500 to-red-600'
    },
    {
      title: 'Cyber-Physical',
      description: 'Digital twin and simulation layer',
      color: 'from-orange-500 to-orange-600'
    },
    {
      title: 'Cognition',
      description: 'AI analytics and machine learning',
      color: 'from-yellow-400 to-yellow-500'
    },
    {
      title: 'Configuration',
      description: 'Operational optimization and control',
      color: 'from-lime-400 to-lime-500'
    },
    {
      title: 'Consciousness',
      description: 'Knowledge management and decision support',
      color: 'from-green-500 to-green-600'
    }
  ];

  // Login Screen
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 flex items-center justify-center p-6">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-2xl shadow-xl border border-slate-200 p-8">
            <div className="text-center mb-8">
              <img src={vitaLogo} alt="VITA Platform" className="h-16 mx-auto mb-4" />
              <h1 className="text-2xl font-semibold text-slate-900 mb-2">
                Welcome to VITA Platform
              </h1>
              <p className="text-slate-600">
                Visionary Industrial Technology Architecture
              </p>
            </div>

            <form onSubmit={handleLogin} className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full px-4 py-3 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="seu.email@exemplo.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Senha
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full px-4 py-3 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="••••••••"
                />
              </div>

              {loginError && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                  {loginError}
                </div>
              )}

              <button
                type="submit"
                disabled={isLoggingIn}
                className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 text-white py-3 px-6 rounded-lg font-medium shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isLoggingIn ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Entrando...
                  </>
                ) : (
                  <>
                    <Lock className="w-5 h-5" />
                    Entrar
                  </>
                )}
              </button>
            </form>

            <div className="mt-6 pt-6 border-t border-slate-200 text-center">
              <p className="text-sm text-slate-500">
                Acesso restrito aos pesquisadores autorizados
              </p>
            </div>
          </div>

          <div className="mt-8 text-center text-sm text-slate-600">
            <p>Fernanda Pereira Guidotti Carneiro</p>
            <p className="text-slate-500">Ph.D. in Computer Science – USP</p>
          </div>
        </div>
      </div>
    );
  }

  // Dashboard Screen
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">
      {/* Header */}
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <img src={vitaLogo} alt="VITA Platform" className="h-12" />
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2 text-slate-700 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors"
            >
              <LogOut className="w-4 h-4" />
              Sair
            </button>
          </div>
          <p className="mt-3 text-slate-600 max-w-3xl">
            A modular AI platform based on the 6C Architecture for intelligent industrial systems.
          </p>
        </div>
      </header>

      {/* Main Section */}
      <main className="max-w-7xl mx-auto px-6 py-12">
        <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Left Side - Controls */}
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold text-slate-900 mb-2">
                  AI Vision Module
                </h2>
                <p className="text-slate-600">
                  Upload an image and run AI-powered object detection.
                </p>
              </div>

              {/* Upload Area */}
              <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                className={`border-2 border-dashed rounded-xl p-8 text-center transition-all ${
                  isDragging
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-slate-300 bg-slate-50 hover:border-slate-400'
                }`}
              >
                <input
                  type="file"
                  id="file-upload"
                  accept="image/*"
                  className="hidden"
                  onChange={(e) => {
                    const file = e.target.files?.[0];
                    if (file) handleFileSelect(file);
                  }}
                />
                <label htmlFor="file-upload" className="cursor-pointer">
                  <Upload className="w-12 h-12 mx-auto mb-4 text-slate-400" />
                  <p className="text-slate-700 font-medium mb-1">
                    Drag and drop or click to upload
                  </p>
                  <p className="text-sm text-slate-500">
                    PNG, JPG up to 10MB
                  </p>
                </label>
              </div>

              {selectedImage && (
                <div className="text-sm text-slate-600 bg-slate-50 rounded-lg p-3">
                  Selected: <span className="font-medium">{selectedImage.name}</span>
                </div>
              )}

              {/* Model Selector */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Detection Model
                </label>
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  className="w-full px-4 py-3 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="yolov3-tiny">YOLOv3 Tiny (Fast)</option>
                  <option value="yolov3">YOLOv3 (Accurate)</option>
                </select>
              </div>

              {/* Run Button */}
              <button
                onClick={handleRunDetection}
                disabled={!selectedImage || isProcessing}
                className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 text-white py-3 px-6 rounded-lg font-medium shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isProcessing ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    Run Detection
                  </>
                )}
              </button>
            </div>

            {/* Right Side - Preview */}
            <div className="space-y-6">
              {/* Original Image */}
              {previewUrl && (
                <div>
                  <h3 className="text-sm font-medium text-slate-700 mb-2">Original Image</h3>
                  <div className="rounded-lg overflow-hidden border border-slate-200 bg-slate-100">
                    <img
                      src={previewUrl}
                      alt="Original"
                      className="w-full h-auto"
                    />
                  </div>
                </div>
              )}

              {/* Result Image */}
              {resultUrl && (
                <div>
                  <h3 className="text-sm font-medium text-slate-700 mb-2">Detection Result</h3>
                  <div className="rounded-lg overflow-hidden border-2 border-green-500 bg-slate-100">
                    <img
                      src={resultUrl}
                      alt="Detection Result"
                      className="w-full h-auto"
                    />
                  </div>
                </div>
              )}

              {!previewUrl && (
                <div className="h-full flex items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-lg min-h-[300px]">
                  <div className="text-center">
                    <Upload className="w-16 h-16 mx-auto mb-2 opacity-30" />
                    <p>Upload an image to start</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* 6C Architecture Section */}
        <div className="mt-16">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-semibold text-slate-900 mb-3">
              6C Architecture for Industrial AI
            </h2>
            <p className="text-slate-600 max-w-2xl mx-auto mb-6">
              A comprehensive framework for implementing intelligent systems in industrial environments.
            </p>
            <a
              href={`${API_URL}/html/docs`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-lg font-medium shadow-lg hover:shadow-xl transition-all hover:scale-105"
            >
              <BookOpen className="w-5 h-5" />
              View Full Documentation
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {architectureLayers.map((layer, index) => (
              <div
                key={index}
                className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className={`inline-block px-3 py-1 rounded-full bg-gradient-to-r ${layer.color} text-white text-sm font-medium mb-3`}>
                  Layer {index + 1}
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2">
                  {layer.title}
                </h3>
                <p className="text-sm text-slate-600">
                  {layer.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white/80 backdrop-blur-sm mt-20">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center">
            <p className="text-slate-900 font-medium mb-1">
              Fernanda Pereira Guidotti Carneiro
            </p>
            <p className="text-slate-600 text-sm mb-2">
              Ph.D. in Computer Science – University of São Paulo
            </p>
            <p className="text-slate-500 text-xs">
              Developed as part of doctoral research on AI in industry
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}