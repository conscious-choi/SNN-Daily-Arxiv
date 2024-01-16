# https://paperswithcode-client.readthedocs.io/en/latest/
from paperswithcode import PapersWithCodeClient

"""
client = PapersWithCodeClient()
papers = client.paper_list("spiking neural networks")
import pdb; pdb.set_trace();
(Pdb) papers.__dict__.keys()
    dict_keys(['count', 'next_page', 'previous_page', 'results'])
(Pdb) len(papers.results)
    50
(Pdb) papers.results[0].__dict__.keys()
    dict_keys(['id', 'arxiv_id', 'nips_id', 'url_abs', 'url_pdf', 'title', 'abstract', 'authors', 'published', 'conference', 'conference_url_abs', 'conference_url_pdf', 'proceeding'])
(Pdb) papers.results[0].id
'going-deeper-in-spiking-neural-networks-vgg'
(Pdb) papers.results[0].arxiv_id
'1802.02627'
(Pdb) papers.results[0].nips_id
(Pdb) papers.results[0].nips_id
(Pdb) papers.results[0].conference
(Pdb) papers.results[0].conference_url_abs
(Pdb) papers.results[0].conference_url_pdf
"""

# neither link or arxiv_id can be searched
"""
client = PapersWithCodeClient()
papers = client.paper_list('http://arxiv.org/abs/2401.06563v1')
import pdb; pdb.set_trace();
(Pdb) papers
Papers(count=0, next_page=None, previous_page=None, results=[])
(Pdb)
"""

# title can be searched
"""
client = PapersWithCodeClient()
papers = client.paper_list('Resource-Efficient Gesture Recognition using Low-Resolution Thermal Camera via Spiking Neural Networks and Sparse Segmentation')
import pdb; pdb.set_trace();
(Pdb) papers
Papers(count=1, next_page=None, previous_page=None, results=[Paper(id='resource-efficient-gesture-recognition-using', arxiv_id='2401.06563', nips_id=None, url_abs='https://arxiv.org/abs/2401.06563v1', url_pdf='https://arxiv.org/pdf/2401.06563v1.pdf', title='Resource-Efficient Gesture Recognition using Low-Resolution Thermal Camera via Spiking Neural Networks and Sparse Segmentation', abstract='This work proposes a novel approach for hand gesture recognition using an inexpensive, low-resolution (24 x 32) thermal sensor processed by a Spiking Neural Network (SNN) followed by Sparse Segmentation and feature-based gesture classification via Robust Principal Component Analysis (R-PCA). Compared to the use of standard RGB cameras, the proposed system is insensitive to lighting variations while being significantly less expensive compared to high-frequency radars, time-of-flight cameras and high-resolution thermal sensors previously used in literature. Crucially, this paper shows that the innovative use of the recently proposed Monostable Multivibrator (MMV) neural networks as a new class of SNN achieves more than one order of magnitude smaller memory and compute complexity compared to deep learning approaches, while reaching a top gesture recognition accuracy of 93.9% using a 5-class thermal camera dataset acquired in a car cabin, within an automotive context. Our dataset is released for helping future research.', authors=['Lars Keuninckx', 'Wout Mommen', 'Ali Safa'], published=datetime.date(2024, 1, 12), conference=None, conference_url_abs=None, conference_url_pdf=None, proceeding=None)])
(Pdb)"""

# whether which conference gets from papers.results[#].proceeding not .conference (maybe not update)
"""client = PapersWithCodeClient()
papers = client.paper_list("SEW ResNet")
import pdb; pdb.set_trace();
(Pdb) papers.results[0]
Paper(id='spike-based-residual-blocks', arxiv_id='2102.04159', nips_id=None, url_abs='https://arxiv.org/abs/2102.04159v6', url_pdf='https://arxiv.org/pdf/2102.04159v6.pdf', title='Deep Residual Learning in Spiking Neural Networks', abstract='Deep Spiking Neural Networks (SNNs) present optimization difficulties for gradient-based approaches due to discrete binary activation and complex spatial-temporal dynamics. Considering the huge success of ResNet in deep learning, it would be natural to train deep SNNs with residual learning. Previous Spiking ResNet mimics the standard residual block in ANNs and simply replaces ReLU activation layers with spiking neurons, which suffers the degradation problem and can hardly implement residual learning. In this paper, we propose the spike-element-wise (SEW) ResNet to realize residual learning in deep SNNs. We prove that the SEW ResNet can easily implement identity mapping and overcome the vanishing/exploding gradient problems of Spiking ResNet. We evaluate our SEW ResNet on ImageNet, DVS Gesture, and CIFAR10-DVS datasets, and show that SEW ResNet outperforms the state-of-the-art directly trained SNNs in both accuracy and time-steps. Moreover, SEW ResNet can achieve higher performance by simply adding more layers, providing a simple method to train deep SNNs. To our best knowledge, this is the first time that directly training deep SNNs with more than 100 layers becomes possible. Our codes are available at https://github.com/fangwei123456/Spike-Element-Wise-ResNet.', authors=['Yanqi Chen', 'Yonghong Tian', 'Tiejun Huang', 'Timothée Masquelier', 'Zhaofei Yu', 'Wei Fang'], published=datetime.date(2021, 2, 8), conference=None, conference_url_abs='http://proceedings.neurips.cc/paper/2021/hash/afe434653a898da20044041262b3ac74-Abstract.html', conference_url_pdf='http://proceedings.neurips.cc/paper/2021/file/afe434653a898da20044041262b3ac74-Paper.pdf', proceeding='neurips-2021-12')"""

# below case not showing conference even this is eccv
"""
client = PapersWithCodeClient()
papers = client.paper_list("Exploring Lottery Ticket Hypothesis in Spiking Neural Networks")
import pdb; pdb.set_trace();
(Pdb) papers
Papers(count=1, next_page=None, previous_page=None, results=[Paper(id='lottery-ticket-hypothesis-for-spiking-neural', arxiv_id='2207.01382', nips_id=None, url_abs='https://arxiv.org/abs/2207.01382v2', url_pdf='https://arxiv.org/pdf/2207.01382v2.pdf', title='Exploring Lottery Ticket Hypothesis in Spiking Neural Networks', abstract='Spiking Neural Networks (SNNs) have recently emerged as a new generation of low-power deep neural networks, which is suitable to be implemented on low-power mobile/edge devices. As such devices have limited memory storage, neural pruning on SNNs has been widely explored in recent years. Most existing SNN pruning works focus on shallow SNNs (2~6 layers), however, deeper SNNs (>16 layers) are proposed by state-of-the-art SNN works, which is difficult to be compatible with the current SNN pruning work. To scale up a pruning technique towards deep SNNs, we investigate Lottery Ticket Hypothesis (LTH) which states that dense networks contain smaller subnetworks (i.e., winning tickets) that achieve comparable performance to the dense networks. Our studies on LTH reveal that the winning tickets consistently exist in deep SNNs across various datasets and architectures, providing up to 97% sparsity without huge performance degradation. However, the iterative searching process of LTH brings a huge training computational cost when combined with the multiple timesteps of SNNs. To alleviate such heavy searching cost, we propose Early-Time (ET) ticket where we find the important weight connectivity from a smaller number of timesteps. The proposed ET ticket can be seamlessly combined with a common pruning techniques for finding winning tickets, such as Iterative Magnitude Pruning (IMP) and Early-Bird (EB) tickets. Our experiment results show that the proposed ET ticket reduces search time by up to 38% compared to IMP or EB methods. Code is available at Github.', authors=['Priyadarshini Panda', 'Ruokai Yin', 'Yeshwanth Venkatesha', 'Hyoungseob Park', 'Yuhang Li', 'Youngeun Kim'], published=datetime.date(2022, 7, 4), conference=None, conference_url_abs=None, conference_url_pdf=None, proceeding=None)])
"""

client = PapersWithCodeClient()

def proceeder(title):
    paper = client.paper_list(title)
    if paper.count != 0:
        pwc = paper.results[0]
        if pwc.proceeding != None:
            return pwc.proceeding
    else:
        return None
    
    