import numpy as np
from typing import List, Dict, Optional, Tuple, Any
import math

class TechnicalAnalyzer:
    """Класс для технического анализа криптовалют"""
    
    @staticmethod
    def calculate_sma(prices: List[float], period: int) -> List[float]:
        """Простая скользящая средняя (Simple Moving Average)"""
        if len(prices) < period:
            return []
        
        sma_values = []
        for i in range(period - 1, len(prices)):
            sma = sum(prices[i - period + 1:i + 1]) / period
            sma_values.append(sma)
        
        return sma_values
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> List[float]:
        """Экспоненциальная скользящая средняя (Exponential Moving Average)"""
        if len(prices) < period:
            return []
        
        ema_values = []
        multiplier = 2 / (period + 1)
        
        # Первое значение EMA равно SMA
        ema = sum(prices[:period]) / period
        ema_values.append(ema)
        
        for i in range(period, len(prices)):
            ema = (prices[i] * multiplier) + (ema * (1 - multiplier))
            ema_values.append(ema)
        
        return ema_values
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> List[float]:
        """Индекс относительной силы (Relative Strength Index)"""
        if len(prices) < period + 1:
            return []
        
        rsi_values = []
        gains = []
        losses = []
        
        # Вычисляем изменения цены
        for i in range(1, len(prices)):
            change = prices[i] - prices[i - 1]
            gains.append(max(change, 0))
            losses.append(max(-change, 0))
        
        # Вычисляем средние значения
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        # Первое значение RSI
        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)
        
        # Вычисляем остальные значения RSI
        for i in range(period, len(gains)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            
            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)
        
        return rsi_values
    
    @staticmethod
    def calculate_bollinger_bands(prices: List[float], period: int = 20, std_dev: float = 2) -> Dict[str, List[float]]:
        """Полосы Боллинджера (Bollinger Bands)"""
        if len(prices) < period:
            return {"upper": [], "middle": [], "lower": []}
        
        sma_values = TechnicalAnalyzer.calculate_sma(prices, period)
        upper_band = []
        lower_band = []
        
        for i in range(len(sma_values)):
            start_idx = i
            end_idx = start_idx + period
            if end_idx > len(prices):
                break
            
            # Вычисляем стандартное отклонение
            subset = prices[start_idx:end_idx]
            std = np.std(subset)
            
            upper = sma_values[i] + (std_dev * std)
            lower = sma_values[i] - (std_dev * std)
            
            upper_band.append(upper)
            lower_band.append(lower)
        
        return {
            "upper": upper_band,
            "middle": sma_values,
            "lower": lower_band
        }
    
    @staticmethod
    def calculate_macd(prices: List[float], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Dict[str, List[float]]:
        """MACD (Moving Average Convergence Divergence)"""
        if len(prices) < slow_period:
            return {"macd": [], "signal": [], "histogram": []}
        
        ema_fast = TechnicalAnalyzer.calculate_ema(prices, fast_period)
        ema_slow = TechnicalAnalyzer.calculate_ema(prices, slow_period)
        
        # Вычисляем MACD линию
        macd_line = []
        min_length = min(len(ema_fast), len(ema_slow))
        
        for i in range(min_length):
            macd_value = ema_fast[i] - ema_slow[i]
            macd_line.append(macd_value)
        
        # Вычисляем сигнальную линию
        signal_line = TechnicalAnalyzer.calculate_ema(macd_line, signal_period)
        
        # Вычисляем гистограмму
        histogram = []
        min_length = min(len(macd_line), len(signal_line))
        
        for i in range(min_length):
            hist_value = macd_line[i] - signal_line[i]
            histogram.append(hist_value)
        
        return {
            "macd": macd_line,
            "signal": signal_line,
            "histogram": histogram
        }
    
    @staticmethod
    def calculate_stochastic(prices: List[float], high_prices: List[float], low_prices: List[float], 
                           k_period: int = 14, d_period: int = 3) -> Dict[str, List[float]]:
        """Стохастический осциллятор"""
        if len(prices) < k_period:
            return {"k": [], "d": []}
        
        k_values = []
        
        for i in range(k_period - 1, len(prices)):
            highest_high = max(high_prices[i - k_period + 1:i + 1])
            lowest_low = min(low_prices[i - k_period + 1:i + 1])
            current_price = prices[i]
            
            if highest_high == lowest_low:
                k = 50  # Нейтральное значение
            else:
                k = ((current_price - lowest_low) / (highest_high - lowest_low)) * 100
            
            k_values.append(k)
        
        # Вычисляем %D (сглаженная %K)
        d_values = TechnicalAnalyzer.calculate_sma(k_values, d_period)
        
        return {
            "k": k_values,
            "d": d_values
        }
    
    @staticmethod
    def get_support_resistance(prices: List[float], window: int = 20) -> Dict[str, List[float]]:
        """Определение уровней поддержки и сопротивления"""
        if len(prices) < window:
            return {"support": [], "resistance": []}
        
        support_levels = []
        resistance_levels = []
        
        for i in range(window, len(prices) - window):
            current_price = prices[i]
            left_window = prices[i - window:i]
            right_window = prices[i + 1:i + window + 1]
            
            # Проверяем на локальный минимум (поддержка)
            if all(current_price <= price for price in left_window) and all(current_price <= price for price in right_window):
                support_levels.append(current_price)
            
            # Проверяем на локальный максимум (сопротивление)
            if all(current_price >= price for price in left_window) and all(current_price >= price for price in right_window):
                resistance_levels.append(current_price)
        
        return {
            "support": support_levels,
            "resistance": resistance_levels
        }
    
    @staticmethod
    def calculate_atr(high_prices: List[float], low_prices: List[float], close_prices: List[float], period: int = 14) -> List[float]:
        """Average True Range (ATR)"""
        if len(high_prices) < period + 1:
            return []
        
        true_ranges = []
        
        for i in range(1, len(high_prices)):
            high_low = high_prices[i] - low_prices[i]
            high_close = abs(high_prices[i] - close_prices[i - 1])
            low_close = abs(low_prices[i] - close_prices[i - 1])
            
            true_range = max(high_low, high_close, low_close)
            true_ranges.append(true_range)
        
        # Вычисляем ATR как EMA от True Range
        atr_values = TechnicalAnalyzer.calculate_ema(true_ranges, period)
        
        return atr_values
    
    @staticmethod
    def get_trend_analysis(prices: List[float], sma_short: int = 20, sma_long: int = 50) -> Dict[str, str]:
        """Анализ тренда на основе скользящих средних"""
        if len(prices) < sma_long:
            return {"trend": "недостаточно данных", "strength": "неизвестно"}
        
        sma_short_values = TechnicalAnalyzer.calculate_sma(prices, sma_short)
        sma_long_values = TechnicalAnalyzer.calculate_sma(prices, sma_long)
        
        if not sma_short_values or not sma_long_values:
            return {"trend": "недостаточно данных", "strength": "неизвестно"}
        
        current_short = sma_short_values[-1]
        current_long = sma_long_values[-1]
        previous_short = sma_short_values[-2] if len(sma_short_values) > 1 else current_short
        previous_long = sma_long_values[-2] if len(sma_long_values) > 1 else current_long
        
        # Определяем тренд
        if current_short > current_long and previous_short > previous_long:
            trend = "восходящий"
        elif current_short < current_long and previous_short < previous_long:
            trend = "нисходящий"
        else:
            trend = "боковой"
        
        # Определяем силу тренда
        price_change = ((prices[-1] - prices[0]) / prices[0]) * 100
        if abs(price_change) > 20:
            strength = "сильный"
        elif abs(price_change) > 10:
            strength = "умеренный"
        else:
            strength = "слабый"
        
        return {
            "trend": trend,
            "strength": strength,
            "price_change_percent": round(price_change, 2)
        }
    
    @staticmethod
    def get_volume_analysis(prices: List[float], volumes: List[float]) -> Dict[str, str]:
        """Анализ объема торгов"""
        if len(prices) < 2 or len(volumes) < 2:
            return {"volume_trend": "недостаточно данных", "price_volume_correlation": "неизвестно"}
        
        # Определяем тренд объема
        recent_volume_avg = sum(volumes[-5:]) / 5 if len(volumes) >= 5 else sum(volumes) / len(volumes)
        earlier_volume_avg = sum(volumes[:-5]) / 5 if len(volumes) >= 10 else sum(volumes) / len(volumes)
        
        if recent_volume_avg > earlier_volume_avg * 1.2:
            volume_trend = "растущий"
        elif recent_volume_avg < earlier_volume_avg * 0.8:
            volume_trend = "падающий"
        else:
            volume_trend = "стабильный"
        
        # Корреляция цены и объема
        price_changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        volume_changes = [volumes[i] - volumes[i-1] for i in range(1, len(volumes))]
        
        if len(price_changes) == len(volume_changes):
            correlation = np.corrcoef(price_changes, volume_changes)[0, 1]
            
            if correlation > 0.7:
                price_volume_correlation = "сильная положительная"
            elif correlation > 0.3:
                price_volume_correlation = "умеренная положительная"
            elif correlation < -0.7:
                price_volume_correlation = "сильная отрицательная"
            elif correlation < -0.3:
                price_volume_correlation = "умеренная отрицательная"
            else:
                price_volume_correlation = "слабая"
        else:
            price_volume_correlation = "неизвестно"
        
        return {
            "volume_trend": volume_trend,
            "price_volume_correlation": price_volume_correlation
        }
    
    @staticmethod
    def analyze(historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Полный технический анализ исторических данных"""
        if not historical_data or len(historical_data) < 20:
            return {"error": "Недостаточно данных для анализа"}
        
        # Извлекаем цены
        prices = [item.get('price', 0) for item in historical_data]
        
        # Вычисляем индикаторы
        sma_20 = TechnicalAnalyzer.calculate_sma(prices, 20)
        sma_50 = TechnicalAnalyzer.calculate_sma(prices, 50)
        rsi = TechnicalAnalyzer.calculate_rsi(prices, 14)
        macd = TechnicalAnalyzer.calculate_macd(prices)
        bollinger = TechnicalAnalyzer.calculate_bollinger_bands(prices)
        
        # Анализ тренда
        trend_analysis = TechnicalAnalyzer.get_trend_analysis(prices)
        
        # Анализ объема (если есть данные)
        volumes = [item.get('volume', 0) for item in historical_data]
        volume_analysis = TechnicalAnalyzer.get_volume_analysis(prices, volumes) if any(volumes) else {}
        
        return {
            "sma_20": sma_20[-1] if sma_20 else None,
            "sma_50": sma_50[-1] if sma_50 else None,
            "rsi": rsi[-1] if rsi else None,
            "macd": {
                "macd": macd["macd"][-1] if macd["macd"] else None,
                "signal": macd["signal"][-1] if macd["signal"] else None,
                "histogram": macd["histogram"][-1] if macd["histogram"] else None
            },
            "bollinger_bands": {
                "upper": bollinger["upper"][-1] if bollinger["upper"] else None,
                "middle": bollinger["middle"][-1] if bollinger["middle"] else None,
                "lower": bollinger["lower"][-1] if bollinger["lower"] else None
            },
            "trend_analysis": trend_analysis,
            "volume_analysis": volume_analysis
        } 