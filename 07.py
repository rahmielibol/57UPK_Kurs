from brian2 import * #Kütüphanelerin tanımlanması
from numpy import * #Numeric python kütüphanesi temel matematiksel işlemlerin fonksiyonları
from matplotlib.pyplot import * #Grafik çizdirme için gerekli kütüphane

start_scope()
#Topla ve ateşle modelinin tanımlanması
#tau = 5*ms #tau değişkenine değer atama(Birimlere dikkat!)
a=-1
b=1
N=2 #hucre sayisi
# Çok satırlı ifadeleri yazmak için ''' kullanılır. Hücre denklemi bu şekilde tanımlanır.
eqs = ''' 
dv/dt = (a*v+b)/tau : 1
tau : second
'''
G = NeuronGroup(N, eqs, threshold='v>0.8', reset='v = 0', method='linear')
G.v=0     #Baslangic kosulu
G.tau=[1*ms,10*ms]
# Modeli gerçekleyen temel fonksiyon hücre sayısı, denklemi, çözüm metodu gibi değişkenlere sahiptir.
M = StateMonitor(G, 'v', record=True)
# Model çalıştırıldığında tüm veriler tutulmaz. StateMonitor gibi fonksiyonlarla kaydedilmek istenen değişkenler seçilir.

# Ateşlemelerin tutulmasını sağlayan fonksiyon.
spikemon = SpikeMonitor(G)

w=0.2 #sinaptik agirlik
S = Synapses(G, G, on_pre='v_post += w') #Sinaps denklemi G'den G'ye presinaptik
#neuron ateşlediğinde post sinaptik neuronun v'si 0.2 artacak şekilde tanımlanmış.
S.connect(i=0, j=1) #Ve G'den G'ye olan bağlantı özelleştirilmiş.
#Bu ifade de i kaynak neuronun indisini, j ise hedef neuronun indisini verir.


run(30*ms)
# Model run komut ile belli bir süre işletilir. (Burada programın akışına dikkat!)

plot(M.t/ms, M.v[0], 'k',label='Neuron 0')
# Kaydedilen veri grafiğe çizdirilir.
plot(M.t/ms, M.v[1], 'r',label='Neuron 1')
xlabel('Time (ms)')
ylabel('v')
legend()
show()
