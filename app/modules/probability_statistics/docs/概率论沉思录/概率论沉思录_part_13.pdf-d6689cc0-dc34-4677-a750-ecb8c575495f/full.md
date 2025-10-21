同样麻烦的足,无论如何定义稳健性/抗异性,都必须付出代价——模型正确时效果较差的代价。事实上,效果可能会差很多。因为显然,最稳健的流程——如果只要求稳健性的"最优"流程——是完全无视模型、数据和先验信息,并认为所有参数为0、所有假设为假的流程!我们将不可避免地需要在相互冲突的稳健性与准确性之间做出某种权衡。稳健性/抗异性的倡导者有义务说明他们要求我们接受怎样的权衡,即效果下降多少。

例如,在估计位置参数时,样本中值  $M$  通常被认为是比样本均值更稳健的估计量。但是很明显,这种"稳健性"是以对数据中的大部分相关信息不敏感为代价的。许多不同的数据集有相同的中值,高于或低于样本中值的数可以任意移动而不影响估计值。然而,这些数据中肯定包含与问题高度相关的信息,而这一切都丢失了。我们认为数据分析的全部目的是从数据中尽可能地提取所有信息。

因此,虽然我们同意在某些情况下可能需要稳健性/抗异性,但是我们认为强调它们的效果代价也很大。在历史文献中,通常仅仅基于"稳健"或"抗异"的理由提出某个特定流程,而不提及它们提供的推断效果,更不用说与替代方法的效果比较了。而贝叶斯方法等替代方法虽然由于缺乏稳健性而受到批评,但是没有任何支持性的事实证据。

那些以这种理由批评贝叶斯方法的人只是在表明他们不了解如何使用贝叶斯方法。我们想证明的是,贝叶斯数据分析如果使用得当,可以在需要时自动提供稳健性和抗异性。事实上,由于贝叶斯方法从不丢弃相关信息,这种方式与基于直观的特定流程所做的在定性上一致,但在定量上有所改进。换句话说,目前的稳健统计方法与其他正统统计方法一样,只是对完整贝叶斯分析自动给出的直观近似。

实际上,这种情况与我们在5.6节中讨论的赛马和天气预报的情况非常相似。新信息(那里称为数据)是不确定为真的,我们看到贝叶斯分析如何自动考虑这一点。这里是模型——作为先验信息的一部分——有疑问,但是在原则上没有区别,因为"数据"和"先验信息"只是我们全部证据的两个组成部分,它们以同样方式进入概率论。在本例中,详细的贝叶斯分析揭示了一些非常有趣和意想不到的洞见。

对模型变化没有反应的推理在某种程度上也一定会对数据变化没有反应。这是我们真正想要的吗?我们认为答案是:有时是;也就是,在我们不确定模型但

仍然确定其中参数含义的问题中, 但是如果我们对模型感到确定, 那么在数据分析过程中, 稳健性/抗异性就是我们最不想要的, 它会因丢弃强有力的信息而浪费数据.

同样, 在对问题做出判断之前, 我们必须明确注意相应的先验信息. 如下所示, 如果选择我们的抽样分布来如实地表示我们对生成数据现象的先验知识, 那么贝叶斯分析会在我们不确定模型时自动为我们提供稳健性/抗异性, 并在我们确定模型时自动提供最优效果.

然而我们可以做出让步, 图基类型的直观工具能勉强考虑各种特殊、一次性的暂时应急手段, 难以——也不适合——构建到模型中. 正式的概率模型应该描述非暂时的情况, 这些情况值得仔细处理和记录以备将来使用. 正如一位数学家曾经说过的那样: "方法是你使用两次的工具."

但是这种一次性的直觉工具必然也是一种个人流程, 因为它没有提供任何理论依据或最优性准则来说明它所做的事情, 以便其他人可以判断其适用性. 如果我们的直觉不同, 那么没有理性推理的规范理论, 我们就将陷入无法解决矛盾的僵局. 但是逻辑上一致的"理性推理的规范理论"由于考克斯定理的存在必然是一种贝叶斯理论.

让我们首先研究最常见情况的贝叶斯处理, 其中数据只分为好坏两类

# 21.3 双模模型

假设我们有一个"好"的抽样分布

$$
G(x|\theta) \tag{21.2}
$$

带有我们想要估计的参数  $\theta$ . 从  $G(x|\theta)$  中获取的数据称为"好"数据. 但也有一个"坏"的抽样分布

$$
B(x|\eta), \tag{21.3}
$$

其中可能包含一个我们不感兴趣的参数  $\eta$ . 来自  $B(x|\eta)$  的数据称为"坏"数据, 它们对于估计  $\theta$  显得没用或者只会使其估计更糟, 因为它们发生的概率与  $\theta$  无关. 我们的数据集由  $n$  个观测值

$$
D = \{x_{1},\dots ,x_{n}\} , \tag{21.4}
$$

组成. 但问题是这些数据有好有坏, 我们不知道哪些是好的 (不过或许可以做出猜测: 一个明显的离群值—— $G(x|\theta)$  长尾处, 或者  $G(x|\theta) \ll B(x|\eta)$  区域中的任何数据——是坏的).

然而在各种实际问题中, 我们可能有一些关于确定给定数据好坏的先验信息.

分配好/坏选择过程的概率可以表达该信息.例如,我们可以定义

$$
q_{i}\equiv { \begin{array}{l l}{1,} & {\mathrm{~i~}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{J}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{A}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{S}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{L}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{O}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{H}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{P}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{II}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{III}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{}I\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}I\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathcal{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathcal{I}I\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}I\mathbb{\mathbb{I}}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{II}I\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbf{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbf{I}I\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}\mathbb{I}
$$

然后分配联合先验概率

给  $2^{n}$  个可能的好坏序列

# 21.4 可交换选择

让我们考虑最常见的情况,关于好/坏选择过程的信息可以通过分配可交换先验来表示.也就是说,任何  $n$  个好/坏序列的概率仅依赖于好和坏的数量  $r$  和  $n - r$  ,而不依赖于它们出现的特定试验.那么分布(21.6)对于  $q_{i}$  的排列是不变的,根据德菲内蒂表示定理(第18章),它由单个生成函数  $g(u)$  确定:

$$
p(q_{1},\dots ,q_{n}|I) = \int_{0}^{1}\mathrm{d}u u^{n}(1 - u)^{n - r}g(u). \tag{21.7}
$$

这很像抛一枚未知偏差的硬币,其中我们说"正面"与"反面",而不是"好"与"坏"。这里有一个参数  $u$ ,如果  $u$  已知,我们会说任意给定数据  $x$  可能以概率  $u$  来自好的分布,或者以概率  $1 - u$  来自坏的分布。因此, $u$  代表的是我们数据的"纯度",越接近1越好。但是  $u$  是未知的,目前  $g(u)$  可以被认为是它的先验概率密度(事实上,拉普拉斯已经这么做了。关于这种表示的更多技术细节见第18章)。因此,我们的抽样分布可以写成好坏分布的概率混合:

实际上,通常的二元假设检验问题是模型(21.8)的特例,其中我们开始知道所有观测值都来自  $G$  或者  $B$ ,但不知道具体是哪个。也就是说, $u$  的先验密度集中在点  $u = 0$ , $u = 1$  上:

$$
p(u|I) = p_{0}\delta (1 - u) + p_{1}\delta (u). \tag{21.9}
$$

$p_{0} = p(H_{0}|I)$ , $p_{1} = 1 - p_{0} = p(H_{1}|I)$  是以下两个假设的先验概率:

$H_{1}\equiv$  所有数据来自分布  $B(x|\eta)$

由于内部参数的存在,这是复合假设。对于这种情况的贝叶斯分析在第4章中已

经简要提到. 当然, 我们在这里所做事情的逻辑并不依赖于 "好" 与 "坏" 的价值判断.

现在假定  $u$  未知, 问题变成估计  $\theta$  的问题. 一个完整的非平凡贝叶斯解往往会很复杂, 因为贝叶斯定理会考虑与问题有哪怕是一点儿相关的每一个因素. 但是通常, 大部分细节对我们所寻求的最终结论几乎没有影响 (这可能只是后验分布的前几矩或百分位数). 这样我们就可以去寻找足够好的有用的近似算法, 这种算法不会丢失基本信息或在非基本信息上浪费计算资源. 可以想象, 这样得出的规则可能是直觉已经提出的规则, 但是鉴于它们是完整最优解的良好数学近似, 它们也可能远优于任何不考虑概率论而发明的直觉工具, 后者取决于直觉有多好.

我们的离群值问题就是这些评论的一个很好例子. 如果好的抽样密度  $G(x|\theta)$  相对  $|x| > 1$  非常小, 而坏的  $B(x|\eta)$  有长尾延伸到  $|x| \geqslant 1$ , 那么任何  $|y| > 1$  的数据  $y$  可以怀疑来自坏分布. 直觉上, 我们应该通过在某种意义上对  $\theta$  的估计少一点儿信念来"对冲我们的赌注". 更具体地说, 如果一条数据的有效性是可疑的, 那么直觉表明, 我们的结论应该对其确切值不那么敏感. 但是我们刚刚说明了稳健性的条件 (直到现在, 这个推理才给出了以前缺少的理论依据). 随着  $|x| \rightarrow +\infty$ , 它实际上肯定是坏的, 直觉可能告诉我们应该完全忽略它.

图基等人早就注意到这种直观的判断, 从而产生了诸如"降序  $\psi$  函数"之类的工具, 它们通过以这种方式修改数据分析算法来实现稳健/抗异性. 这些工作通常要么没有注意到贝叶斯方法的存在, 要么包含对贝叶斯方法的严厉批评, 说贝叶斯方法不稳健/没有抗异性, 而直觉方法的引入正是为了弥补这一缺陷. 但是这些工作中从未提供任何事实证据来支持这一立场.

下面我们将打破数十年的先例, 实际检查贝叶斯方法对离群值效应的计算, 以便人们可以——也许是第一次——看到贝叶斯学派对这个问题的看法, 从而提供缺失的事实证据.

# 21.5 一般贝叶斯解

我们首先给出基于模型 (21.8) 的一般贝叶斯解, 然后研究一些特殊情况. 令  $p(\theta \eta u|I)$  为参数的联合先验密度. 给定数据  $D$  的联合后验密度是

$$
f(\theta , \eta , u|DI) = A f(\theta , \eta , u|I) L(\theta , \eta , u), \tag{21.11}
$$

其中  $A$  是归一化常数, 根据 (21.8),

$$
L(\theta , \eta , u) = \prod_{i = 1}^{n} [u G(x_{i}|\theta) + (1 - u) B(x_{i}|\eta)] \tag{21.12}
$$

是它们的联合似然.  $\theta$  的边缘后验密度为

$$
p(\theta |D I) = \int \int \mathrm{d}\eta \mathrm{d}u f(\theta ,\eta ,u|D I). \tag{21.13}
$$

为了更明确地写出(21.12),对先验密度进行分解:

$$
f(\theta ,\eta ,u|I) = h(\eta ,u|\theta ,I)f(\theta |I), \tag{21.14}
$$

其中  $f(\theta |I)$  是  $\theta$  的先验密度,  $h(\eta ,u|\theta ,I)$  是给定  $\theta$  时  $(\eta ,u)$  的联合先验.那么  $\theta$  的边缘后验密度(包含数据和先验信息提供给我们的所有关于  $\theta$  的信息)为

$$
f(\theta |D,I) = \frac{f(\theta|I)\overline{{L}}(\theta)}{\int\mathrm{d}\theta f(\theta|I)\overline{{L}}(\theta)}, \tag{21.15}
$$

其中我们引人了拟似然

$$
\overline{{L}} (\theta)\equiv \int \int \mathrm{d}\eta \mathrm{d}u L(\theta ,\eta ,u)h(\eta ,u|\theta ,I). \tag{21.16}
$$

将(21.12)插入(21.16)并展开,我们有

$$
\begin{array}{l}{{\overline{{L}}(\theta)=\int\int\mathrm{d}\eta\mathrm{d}u h(\eta,u|\theta,I)\bigg[u^{n}L(\theta)+u^{n-1}(1-u)\sum_{j=1}^{n}B(x_{j}|\eta)L_{j}(\theta)}}\\ {{\qquad+u^{n-2}(1-u)^{2}\sum_{j< k}B(x_{j}|\eta)B(x_{k}|\eta)L_{j k}(\theta)+\cdot\cdot\cdot}}\\ {{\qquad+(1-u)^{n}B(x_{1}|\eta)\cdot\cdot\cdot B(x_{n}|\eta)\bigg],}}\end{array} \tag{21.17}
$$

其中

$$
\begin{array}{l}{{{\cal L}(\theta)\equiv\prod_{i=1}^{n}G(x_{i}|\theta),}}\\ {{{\cal L}_{j}(\theta)\equiv\prod_{i\neq j}G(x_{i}|\theta),}}\\ {{{\cal L}_{i j}(\theta)\equiv\prod_{i\neq j,k}G(x_{i}|\theta),}}\end{array} \tag{21.18}
$$

是我们使用除  $x_{j}$  外、除  $x_{j}$  和  $x_{k}$  等之外所有数据的好分布的似然函数序列.为了解释冗长的(21.17),注意  $L(\theta)$  的系数

$$
\int_{0}^{1}\mathrm{d}u\int \mathrm{d}\eta h(\eta ,u|\theta ,I)u^{n} = \int \mathrm{d}u u^{n}h(u|\theta ,I) \tag{21.19}
$$

是以条件为  $\theta$  和先验信息为所有数据  $\{x_{1},\dots ,x_{n}\}$  都是好数据的概率.这用拉普拉斯- 德菲内蒂形式(21.7)表示,其中生成函数  $g(u)$  是以  $\theta$  为条件的  $u$  的先验密度  $h(u|\theta ,I)$  .当然,在大多数实际问题中,这与  $\theta$  无关(这可能是与  $u$  完全不同的场景中的一些参数),但暂时保持一般性将有助于以后提出一些有趣的观点.

同样,(21.17)中  $L_{j}(\theta)$  的系数为

$$
\int \mathrm{d}u u^{n - 1}(1 - u)\int \mathrm{d}\eta B(x_{j}|\eta)h(\eta ,u|\theta ,I). \tag{21.20}
$$

现在,因子

$$
\mathrm{d}\eta \int \mathrm{d}u u^{n - 1}(1 - u)h(\eta ,u|\theta I) \tag{21.21}
$$

是给定  $I$  和  $\theta$  ,某一指定数据  $x_{j}$  为环,其他  $n - 1$  个数据为好,并且  $\eta$  位于  $(\eta ,\eta +\mathrm{d}\eta)$  区间内的联合概率密度.因此,系数(21.20)是在给定  $I$  和  $\theta$  的情况下,第  $j$  个数据为坏且值为  $x_{j}$  ,而其他数据为好的概率.这样继续下去,我们看到,用通俗语言描述,我们的拟似然是

$\overline{{L}} (\theta) =$  (所有数据是好的概率)  $\times$  (使用所有数据的似然)

$+\sum_{j}$  (只有  $x_{j}$  是坏的概率)  $\times$  (使用除了  $x_{j}$  之外的似然)

$+\sum_{j,k}$  (只有  $x_{j},x_{k}$  是坏的概率)  $\times$  (使用除了  $x_{j},x_{k}$  之外的似然) (21.22)

十

$+\sum_{j}$  (只有  $x_{j}$  是好的概率)  $\times$  (只使用数据  $x_{j}$  的似然)

$+$  (所有数据是坏的概率).

简而言之:拟似然  $\overline{{L}} (\theta)$  是好分布  $G(x|\theta)$  似然的加权平均值.这是关于数据好坏的所有的可能假设,根据这些假设的先验概率加权结果.我们看到贝叶斯解如何考虑了我们关于数据生成先验知识的每个细节.

这个结果的范围如此之广,以至于需要大量篇幅来研究其所有含义及有用情形,但是让我们注意最简单的情况并将其与我们的直觉做比较.

# 21.6 确定异常值

假设好数据的分布集中在一个有限区间

$$
G(x|\theta) = 0,\qquad |x| > 1, \tag{21.23}
$$

而坏数据分布在包含这一区间的更宽区间内是正的.那么任何  $|x| > 1$  的数据  $r$  肯定是一个异常值,即坏数据.如果  $|x|< 1$  ,我们无法确定它是好是坏.在这种情况下,我们的直觉非常有力地告诉我们:任何已知为坏的数据都与估计  $\theta$  不相关,我们根本不应该考虑它,因此,只需要将其丢弃并根据剩余数据进行估计.

根据贝叶斯定理,这几乎是正确的.假设我们发现  $x_{j} = 1.432,x_{k} = 2.176$

并且所有其他  $u$  都小于 1,那么观察 (21.24) 可以看到只有项会保存下来:

$$
\bar{L} (\theta) = \int \mathrm{d}u \int \mathrm{d}\eta h(\eta , u|\theta I) B(x_{j}|\eta) B(x_{k}|\eta) L_{jk}(\theta) = C_{jk}(\theta) L_{jk}(\theta). \tag{21.24}
$$

如上所述,因子  $C_{jk}$  几乎总是与  $\theta$  无关,并且由于常数因子与似然无关,我们在 (21.15) 中的拟似然简化为丢弃异常值获得的似然,与直觉一致.

但是可以想象,在极少数情况下,  $C_{jk}(\theta)$  仍然可能依赖于  $\theta$ . 贝叶斯定理告诉我们,这种情况将会有所不同. 如果我们深入思考,会明白结果其实是在意料之中的. 因为如果获取两个值为  $x_{j}, x_{k}$  的异常值的概率依赖于  $\theta$ ,那么我们得到这些异常值的事实本身就是与  $\theta$  的推断相关的证据.

因此,即使在这种简单情况下,贝叶斯定理也会告诉我们一些凭借简单直觉看不到的东西:即使已知某些数据是异常值,它们的值原则上仍然有可能与  $\theta$  的估计相关. 这就是我们所说的贝叶斯定理会考虑与问题相关的每一个因素的意思.

在更一般的情况下,贝叶斯定理告诉我们,当已知任何数据为异常值时,如果获得该特定异常数据的概率与  $\theta$  无关,那么我们应该简单地将其丢弃. 因为一般来说,只有当所有  $\theta$  的  $G(x_{i}|\theta) = 0$  时,才能确切知道数据  $x_{i}$  是异常值. 在这种情况下,(21.24) 中包含  $x_{i}$  的每个似然都将为 0,并且我们对  $\theta$  的后验分布将与从未观察到数据  $x_{i}$  一样.

# 21.7 一个远离值

现在假设我们感兴趣的是一个位置参数,并且有一个包含 10 个观测值的样本,但是其中一个数据  $x_{j}$  远离其他数据构成的聚类,最终偏离好分布  $G$  100 个标准差. 我们对  $\theta$  的估计将如何考虑它?答案依赖于我们指定的模型.

考虑一般的模型,其中抽样分布被简单地视为  $G(x|\theta)$ ,没有提及任何其他"坏"分布. 如果  $G$  是高斯分布,  $x \sim N(\theta , \sigma)$ ,并且我们对  $\theta$  的先验很宽(比如大于  $1000\sigma$ ),那么二次损失函数的贝叶斯估计将还是等于样本均值,我们的孤立数据将使估计值与其他 9 个数据值的均值相差约 10 个标准差. 这大概是贝叶斯方法有时被指责为缺乏稳健性/抗异性的原因.

然而,这只是所假设模型的预期结果,它实际上坚持认为:我事先知道  $u = 1$ ,所有数据都来自  $G$ ,我对此非常确定,数据中的任何证据都无法改变我的想法. 如果一个入真的有这么强的先验知识,那么这个离群数据将是非常重要的,将其作为"异常值"抛弃将忽略强有力的证据,也许是数据中提供的最强有力的证据. 事实上,重要的科学发现往往来自一位对自己的仪器非常有信心的实验者,因此他会相信令人惊讶的新数据,而不仅仅是将其作为"偶然的"异常值而加以拒绝,这

只是一种老生常谈。

然而，如果我们的直觉强烈地告诉我们应该丢弃离群数据，那么我们一定不相信  $u = 1$  足以在面对令人惊讶的数据的证据时坚持它，贝叶斯主义者可以通过使用更现实的模型（21.8）来纠正这一点，这样，对第一个流程的正确批评方式不是贝叶斯方法本身，而是将贝叶斯方法强加在一个武断提出的不灵活模型上，该模型否认异常值存在的可能性.我们在4.4节关于多重假设检验的讨论中看到，当允许机器人对过于简单的模型产生怀疑时，结果会有多大的不同.

贝叶斯方法内在具有所需的稳健性/抗异性，并且会在需要时自动具有这些性质——如果有足够灵活的模型允许它们这样做．但是，如果我们对它们加以荒谬的限制条件，无论是贝叶斯还是任何其他方法都无法给出合理的结果．这里面有一个寓意，涉及所有的概率论．在其他应用数学领域，未能注意到某个特征（例如坏分布  $B$  存在的可能性）仅仅表示不会考虑这些特征．在概率论中，没有注意到某个特征可能等同于对其做出不合理的假设

那么，为什么贝叶斯方法在这个问题上比正统方法受到了更多的批评呢？这是出于与以下情况相同的原因：统计数据表明城市  $B$  的犯罪率高于城市  $A$  ，但是事实是城市  $B$  的犯罪率更低，更高犯罪率的表象是由于该城市检测犯罪的手段更有效．未发现的错误没有被批评

与该领域的其他问题一样，这可以进一步推广和扩展为三模模型，将参数放入(21.6)，等等．但是我们的模型已经足够一般化，同时包含离群值问题和常规假设检验理论．从该模型几个简单示例中可以学到很多东西.

# 第22章 通信理论导论

我们在第11章中特别提出,本书背后的写作动机之一是试图将古布斯统计力学和香农的通信理论视为同一种推理过程的不同示例。- - 1引入熵的概念,就产生了统计力学的广义形式。我们现在应该能够以类似的方式处理通信理论。

两者之间的差别是:在统计力学中,先验信息与频率无关(它由压力等宏观量的测量值组成),因此我们不容易犯错误;但是在通信理论中,先验信息通常由频率组成,这使得人们更容易掉进概率- 频率的概念陷阱之中。出于这个原因,最好先通过简单应用看清概率和频率之间的一般联系,再开始讨论通信理论。

# 22.1 理论起源

首先是给予应得荣誉的难题。思想方面的所有重大进步都有其先驱,而先驱工作的全部意义在当时从未被认识到。最明显的例子是,相对论在马赫、斐兹杰惹、洛伦兹和庞加莱的工作中都有体现。通信理论有许多先驱,在吉布斯、奈奎斯特、哈特利、西拉德、诺依曼和维纳的工作中都有涉及。但是不可否认的是,香农的论文(Shannon,1948)是通信理论诞生的主要标志,就像爱因斯坦1905年的论文标志着相对论的诞生一样。可以这么说,在这两种情况下,长期以来以一种模糊的形式"处在迷雾之中"的想法得到了极大的澄清。

香农的论文中充满了重要的新概念和新成果。它们不仅带给人们刺激,也令人崩溃。在香农的论文出现后的最初几年里,人们普遍听到这样的悲观的声音:香农已经预料并解决了该领域中的所有问题,其他人已经无事可做。

除了少数例外,后香农时代的发展可以归为两个完全不同方向的尝试。在应用方面,我们有扩展主义者(他们试图将香农的想法应用到其他领域,就像我们在这里所做的那样)、熵计算者(他们计算出电视信号、法语、染色体或者几乎任何你能想象到的其他任何东西的熵,然后发现没有人知道如何使用它)和全能主义者(他们确信香农的工作将彻底改变所有智力活动,但是无法提供任何被其改变的具体示例)。

我们不应过分批评这些尝试,因为正如皮尔斯所说的那样:- - 开始其实很难分辨哪些是有意义的,哪些纯属无稽之谈,而哪些又是有意义工作的开始。我自己的工作可以被分到以上所有三类中。我们曾经预期,香农的思想对语言学家、遗

传学家、电视工程师、神经学家和经济学家来说最终都是不可或缺的。但是，让我们与许多人一样感到失望的是，40年来在这方面的尝试在这些领域中取得的真正有用的进展非常少。

在这段时间里，模糊哲学和抽象数学泛滥成灾。但是，除了编码理论外，使用该理论解决具体实际问题的例子少之又少。我们认为，造成这种情况的原因是概念上的误解，几乎所有这些都是由于思维投射谬误阻碍了人们提出正确的问题。为了将通信理论应用于编码以外的其他问题，第一步、同样也是最难的一步，是明确说明我们想要解决的具体问题是什么。

与上述努力目标几乎截然相反的是，一批数学家将通信理论简单视为纯数学的一个分支。该学派的特点是，认为在引入连续概率分布之前必须讨论集合论、博雷尔场、测度论、勒贝格- 斯蒂尔杰斯积分和拉东- 尼科迪姆定理。重要的是按照当时数学家中流行的严格准则使定理变得严格，即使这样做会限制它们的应用范围。辛钦(Khinchin，1957)关于信息论的书就是这种风格的典型例子。

再次强调，我们不需要对这些尝试进行严厉批评。当然，我们希望我们的原则受到人类思想所能施加的最严格标准的审查。如果存在重要的应用，那么对这方面的需求就会更大。然而，本书不是为数学家，而是为关注实际应用的人而写的。因此，我们将只讨论与实际应用相关的方面，并指出严格的定理与现实世界的问题无关。通常，它们描述的情况并不存在（例如无限长的消息），因此通过将概率1分配为不可能事件，而为所有可能事件分配概率0，就变成了“无意义的定理”。我们无法使用这样的结果，因为我们的概率总是以我们对现实世界的了解为条件的。现在讨论香农论文中的一些具体内容。

# 22.2 无噪声信道

我们处理从发送方到接收方的信息传输。下面将用拟人化的术语来谈论它们，例如“接收端的人”，尽管一端或两端实际上可能是机器，如在遥测或遥控系统中。传输通过某一信道进行，这些信道可能是电话或电报电路、微波链路、美国联邦通信委员会（FCC）分配的频段、德语、邮递员、邻居八卦或者染色体。如果在接收到消息后，接收者总能确定发送者想要发送什么消息，我们就说该信道是无噪声的。

在通信理论发展的早期，特别是奈奎斯特和哈特利就认识到，信道的能力不是由它发送的特定消息的性质来描述的，而是由它可以发送的内容来描述的．信道的用处在于它可以传输- 大类消息中的任何一个，发送者可以随意选择.

在无噪声信道中，这种能力的一种显然的度是信道在时间t内能够传输的

(在目的地)可区分消息的最大数量  $W(t)$  。在我们感兴趣的所有情况下,对于足够大的  $t$  ,这个数字最终会呈指数增长:  $W(t) \propto \mathrm{e}^{C t}$  ,因此与任何特定时间间隔无关的信道性能度量是增长系数  $C$  ,我们将信道容量定义为

$$
C \equiv \lim_{t \to +\infty} \left[ \frac{1}{t} \log \left[W(t)\right] \right]. \tag{22.1}
$$

$C$  的单位依赖于我们选择的对数底数,通常以2为底数,这样  $C$  的单位是"比特/秒",1比特是单个二进制(是一吞)位中包含的信息量,为了便于解释,比特是最好的单位,但是在形式运算中,使用自然对数e作为底数可能更方便,这样我们的信道容量就以自然单位或"尼特/秒"来衡量,要进行转换,请注意1比特 $= \ln 2\approx 0.69315$  尼特,或者1尼特  $\approx 1.4427$  比特.

无噪声信道的容量是一个标识信道特征的确定数字,与人类信息无关,因此,如果无噪声信道每秒可以传输从包含  $a$  个字母的字母表中以任意顺序选择的  $n$  个符号,我们就有  $W(t) = a^{n t}$  ,或者  $C = n \log_{2} a$  比特/秒  $= n \ln a$  尼特/秒,对可能字母序列的任何限制只会降低这一数值,如果字母表是  $A_{1}, A_{2}, \dots , A_{a}$  ,并且要求在  $N = n t$  个符号的长消息中,字母  $A_{i}$  一定以相对频率  $f_{i}$  出现,那么在时间  $t$  内可能的消息数量只是

$$
W(t) = \frac{N!}{(N f_{1})!\cdots(N f_{a})!}, \tag{22.2}
$$

根据我们在第11章中描述的斯特林近似,

$$
C = -n \sum_{i} f_{i} \ln f_{i} \text{尼特} / \text{秒}. \tag{22.3}
$$

它在等频率  $f_{i} = 1 / a$  时达到最大值,即之前的  $C = n \ln a$  ,因此,我们得到一个有趣的结果,即所有字母以相同频率出现的约束根本不会减小信道容量,当然,它确实将数量  $W(t)$  减少了很多,但  $\ln W$  的减少是真正重要的,这比  $t$  的增长要慢,所以它在极限时没有差别,根据第11章的集中定理,这可以用另一种方式来理解:在所有可能的消息中,绝大多数字母频率几乎相等.

现在假设符号  $A_{i}$  需要传输时间  $t_{i}$  ,但是对允许的字母序列没有限制,这时信道容量是多大呢?首先考虑字母  $A_{i}$  出现  $n_{i}$  次的消息的情况,其中  $i = 1, 2, \dots , a$  此类消息的数量是

$$
W(n_{1}, \dots , n_{a}) = \frac{N!}{n_{1}!\cdots n_{a}!}, \tag{22.4}
$$

其中

$$
N = \sum_{i = 1}^{a} n_{i}. \tag{22.5}
$$

这样时间  $t$  内可能被传输的不同消息数量是

$$
W(t) = \sum_{n_{i}}W(n_{1},\dots ,n_{n}), \tag{22.6}
$$

其中的求和是对满足  $n_{i}\geqslant 0$  且

$$
\sum_{i = 1}^{a}n_{i}t_{i}\leqslant t \tag{22.7}
$$

的所有可能  $(n_{1},\dots ,n_{a})$  进行的.(22.6)中的项数  $K(t)$  满足  $K(t)\leqslant (B t)^{a}$  ,其中 $B< +\infty$  为常数.通过将  $n_{i}$  想象为  $a$  维空间中的坐标并注意到  $K(t)$  的几何意义为单纯形的体积,这很容易理解.

对(22.6)的准确计算是一项繁冗的工作.但是我们现在只关心它的极限值,这样可以使用以下技巧.注意到  $W(t)$  不会小于(22.6)中的最大项  $\bar{W_{m}} =$ $W_{\max}(n_{1},\dots ,n_{a})$  也不会大于  $W_{m}K(t)$

$$
\ln W_{m}\leqslant \ln W(t)\leqslant \ln W_{m} + a\ln (B t), \tag{22.8}
$$

因此我们有

$$
C\equiv \lim_{t\to +\infty}\frac{1}{t}\ln W(t) = \lim_{t\to +\infty}\frac{1}{t}\ln W_{m}, \tag{22.9}
$$

即为了得到信道容量,在约束条件(22.7)下最大化  $\ln W(n_{1},\dots ,n_{a})$  就足够了.这个相当令人惊讶的事实可以理解如下:  $W(t)$  的对数粗略地由  $\ln W(t) = \log W_{\max}+$ $\ln [(22.6)$  中合理大小项的数量]给出.尽管大项的数量以  $t^{a}$  趋于无限大,但是与 $W_{\max}$  的指数增长相比,这还不够快,无法造成差别.正如薛定谔(Schrödinger,1948)所解释的,基于同样的数学原因,在统计力学中,达尔文- 福勒方法与最概然分布方法在大系统的极限时会得到相同的结果.

我们可以通过与第11章中使用的相同的拉格朗日乘子方法来解决最大化 $\ln W(n_{1},\dots ,n_{a})$  的问题.但是问题并不完全相同,因为现在  $N$  也将在寻找最大值时变化.使用对大  $n_{i}$  有效的斯特林近似,我们有

$$
\ln W(n_{1},\dots ,n_{a})\approx N\ln N - \sum_{i = 1}^{a}n_{i}\ln n_{i}. \tag{22.10}
$$

带拉格朗日乘子  $\lambda$  的变分问题是

$$
\delta \left[\ln W + \lambda \sum n_{i}t_{i}\right] = 0, \tag{22.11}
$$

但是由于  $\delta N = \sum \delta n_{i}$  ,我们有

$$
\delta \ln W = \delta N\ln N - \delta N - \sum_{i}(\delta n_{i}\ln n_{i} - \delta n_{i}) = -\sum \delta n_{i}\ln (n_{i} / N). \tag{22.12}
$$

因此(22.11)简化为

$$
\sum_{i = 1}^{a}\left[\ln \left(\frac{1}{\pi}\left(\frac{1}{\pi}\right) + \lambda t_{i}\right)\delta \tau t_{i} = 0\right], \tag{22.13}
$$

其解为

$$
n_{i} = N\mathrm{e}^{-\lambda t_{i}}. \tag{22.14}
$$

为了固定  $\lambda$  的值,我们需要

$$
N = \sum n_{i} = N\sum \mathrm{e}^{-\lambda t_{i}}. \tag{22.15}
$$

通过这样选择  $n_{i}$ ,我们得到

$$
\frac{1}{t}\ln W_{m} = -\frac{1}{t}\ln (n_{i} / N) = \frac{1}{t}\sum n_{i}(\lambda t_{i}). \tag{22.16}
$$

在  $t^{- 1}\sum n_{i}t_{i}\to 1$  的极限时有

$$
C = \lim_{t\to +\infty}\frac{1}{t}\ln W(t) = \lambda . \tag{22.17}
$$

最终结果可以简单描述为

为了计算符号  $A_{i}$  需要传输时间  $t_{i}$  并且对可能信息没有其他限制的无

噪声信道的容量,定义分拆函数  $Z(\lambda)\equiv \sum_{i}\mathrm{e}^{- \lambda t_{i}}$ ,那么信道容量  $C$  就

是以下方程的实根:

$$
Z(\lambda) = 1. \tag{22.18}
$$

可以看到这里的推理和形式体系与统计力学非常相似,尽管我们还没有谈到任何概率.

根据(22.15),我们看到当符号  $A_{i}$  的相对频率由规范分布

$$
f_{i} = \frac{N_{i}}{N} = \mathrm{e}^{-\lambda t_{i}} = \mathrm{e}^{-C t_{i}} \tag{22.19}
$$

给出时,  $W(n_{1},\dots ,n_{a})$  达到最大化.一些人由此得出结论:当我们对消息进行使得(22.19)成立的编码时,信道将被"最有效地使用".但这其实是错误的,因为在时间  $t$  中,无论我们使用什么相对频率,该信道实际上只会传输一条消息.(22.19)告诉我们的只是一—根据确集中定理——信道在时间  $t$  内可能传输的所有消息中,绝大多数是相对频率典型的消息.

另外,我们对(22.3)之后的评论进行概括:如果额外要求相对频率由(22.19)给出——这可以视为定义了一个新信道——则信道容量不会减小.但是任何要求可能消息具有不同于(22.19)的字母频率的约束将减小信道容量.

有许多其他方式可以解释这些等式.例如,在以上论证中,我们假设传输总时间是固定的,并希望最大化发送者可以选择的可能消息的数量  $W$ 。在实际通信

系统中,情况通常是相反的:我们预先知道可能通过信道发送的消息的选择范围,因此  $W$  是固定的.然后要求在固定  $W$  时使消息的总传输时间最小化的条件.

众所周知,变分问题可以转化为几种不同的形式,许多不同问题的解是同样的数学结果.对于给定的周长,圆具有最大面积;但是在给定面积时,圆也具有最小周长.在统计力学中,规范分布可以表征为对于给定能量期望具有最大熵的分布,或者也是对于给定的熵具有最小能量期望的那个分布.类似地,根据(22.18)得到的信道容量给出了给定的传输时间内最大可达到的  $W$  ,或者对于固定的  $W$  可达到的最小传输时间.

可以对这些等式的含义做另一种扩展:注意我们不需要将  $t_{i}$  解释为时间,它同样可以表示传输第  $i$  个符号的以任何标准度量的"成本".也许信道运行的总时间并不重要,因为无论是否使用,仪器都必须准备就绪.真正的标准可能是太空探测器在将信息传输回地球时必须消耗的能量.在这种情况下,我们可以将  $t_{i}$  定义为传输第  $i$  个符号所需的能量.这样,根据(22.18)给出的信道容量,不是以每秒比特数而是以每焦耳比特数为单位,其倒数是传输1比特信息所需的最小焦耳数.

香农也考虑过一种更复杂的无噪声信道,它是一种有记忆的信道.它可能处于"状态"集合  $\{S_{1},\dots ,S_{k}\}$  中的任意一种状态,并且未来的可能符号或其传输时间依赖于当前状态.例如,假设信道处于状态  $S_{i}$  ,它可以传输符号  $A_{n}$  ,使得信道处于状态  $S_{j}$  ,对应的传输时间为  $t_{i n j}$  .令人惊讶的是,在这种情况下,信道容量的计算非常容易.

令  $W_{i}(t)$  是信道可以在时间  $t$  内从状态  $S_{i}$  开始传输的不同消息的总数.根据传输的第一个符号将  $W_{i}(t)$  分解为几项,我们将得到第9章中用于引入分拆函数的相同差分方程:

$$
W_{i}(t) = \sum_{j n}W_{j}(t - t_{i n j}), \tag{22.20}
$$

其中求和是对所有可能的序列  $S_{i}\to A_{m}\to S_{j}$  进行的.与以前一样,这是一个常系数的线性差分方程,所以它的渐近解一定是指数函数:

$$
W_{i}(t)\approx B_{i}\mathrm{e}^{C t}, \tag{22.21}
$$

显然,根据定义(22.1),系数  $C$  对于有限  $k$  是信道容量.将(22.21)代人(22.20),我们得到

$$
B_{i} = \sum_{j = 1}^{k}Z_{i j}(C)B_{j}, \tag{22.22}
$$

其中

$$
Z_{i j}(\lambda) = \sum_{n}\mathrm{e}^{-\lambda t_{i n j}} \tag{22.23}
$$

组成"配分矩阵",可以将此论证与我们在第9章中对分拆函数的推导进行比较。如果序列  $S_{i} \rightarrow A_{n} \rightarrow S_{j}$  是不可能的,设  $t_{i n j} = +\infty$ 。通过这种方法,我们可以将(22.23)中的求和理解为针对字母表中的所有符号。

(22.22)表明矩阵  $(Z_{i j})$  的特征值等于1,因此信道容量只是方程  $D(\lambda) = 0$  的最大实根,其中

$$
D(\lambda) \equiv \operatorname *{det}[Z_{i j}(\lambda) - \delta_{i j}]. \tag{22.24}
$$

这是香农给出的最漂亮的结果之一。在  $k = 1$  的单一状态时,它简化为先前的规则(22.18)。

以上解决的问题当然只是特别简单的问题。通过构建对允许序列具有更复杂约束的信道(即具有长记忆),我们可以根据需要生成数学问题。但这仍然只是数学问题——只要通道是无噪声的,就不会有原则上的困难。在每种情况下,我们只需要根据不同的可能性应用定义(22.1)重新计算。对于一些奇怪的信道,我们可能会发现其中极限不存在,在这种情况下,我们不能说信道容量,而只能通过给出函数  $W(t)$  来表征信道。

# 22.3 信息来源

当我们进入下一步并考虑为信道提供信息源时,就会出现全新的问题。在我们能说明哪些数学问题重要之前,有大量的数学问题需要考虑,但是也有更基本的概念问题需要考虑。

诺伯特·维纳教授首先提出使用概率术语表示信息源这一卓有成效的想法。他将此应用于滤波器设计中的一些问题。这项工作是发展出一种思维方式的重要一步,最终导致通信理论的诞生。

现在我们可能很难意识到这是多么重大的一步。从前,通信工程师认为信息源只是有消息要发送的人,就其目的而言,可以简单地通过描述该消息来表征信息源。但是维纳指出,信息源的特征在于它发出各种消息  $M_{i}$  的概率  $p_{i}$ 。我们已经看到概率的频率理论所面临的概念上的困难——发送者大概很清楚自己要发送什么消息。那么,我们所说的他发送东西的概率是什么意思呢?这里没有任何类似于"偶然性"的东西。

概率  $p_{i}$  是指他发送特定消息的频率吗?这个说法很荒谬:一个理智的人最多发送一次指定消息,而从不发送其他消息。我们的意思是消息  $M_{i}$  出现在某个想

象的通信行为"集合"中的频率吗?你愿意这么说也没有关系,但是这没有回答我们的问题,这只是将我们的问题重新表述为:是什么定义了该集合?如何设置它?使用不同的名字对我们没有帮助.确  $H = - \sum p_{i}\ln p_{i}$  测量的究竟是什么信息?

如果假设香农的  $H$  衡量的不是发送者的信息,而是接收者的无知(这种无知通过消息的接收消除),那么我们就朝着回答这个问题迈出了满珊的第一步.事实上,大多数后来的评论者做的是这种解释,然而,转念一想,这也没有任何意义,因为香农继续将  $H$  与传输消息  $M_{i}$  所需的信道容量  $C$  相关联发展定理.但是一个信道能多好地传输消息显然依赖于信道和消息的性质,而不是接收者的无知状态!你可以看到这个领域中已经存在40年概念上的混乱.

在这一点上,必须清楚地说明我们想要解决的具体问题是什么,概率分布是描述知识状态的一种手段,但是我们想谈论谁的知识状态?显然不是发送者或接收者的知识状态,香农在这方面没有明确地帮助我们,但是隐含的答案似乎很清楚,香农定理不是像许多人所假设的那样描述发送者和接收者之间通信的"一般原则",他认为该理论对于一名设计通信系统的工程师来说具有实用价值,换言之,香农所描述的知识状态是通信工程师设计设备时的知识状态,  $H$  衡量的是通信工程师对要发送的消息的无知.

虽然这种观点对于贝尔电话实验室的工程师(比如当时的香农)来说似乎非常自然,但这种观点没有在香农的论文或者后来的文献中表述过,后来者往往看不到概率与频率之间的区别,因为在频率论者看来,具有某种知识状态的人的概率这一概念根本不存在,因为概率被认为是一种独立于人类信息而存在的真实物理现象,但是选择某一概率分布来表示信息源的问题仍然存在,这是无法回避的.现在很明显,理论的全部内容依赖于我们如何做到这一点.

我们已经多次强调,我们在概率论中从来不会解决真实的实际问题,我们只解决实际问题的某个抽象数学模型,建立该模型不仅需要数学能力,还需要大量的实践判断,如果我们的模型不能很好地与实际情况保持一致,那么我们的定理,无论数学上多么严格,都可能会误导人而不是提供帮助,这在通信理论中似乎是一种报复,因为不仅是定量的细节,甚至连可以证明的定理的定性性质,都取决于我们使用哪种概率模型来表示信息源.

这一概率模型的目的是描述通信工程师关于他的通信系统可能发送什么消息的先验知识,原则上,这种先验知识可以是任意的,特别是,没有什么阻止它在本质上是语义的,例如,他可能事先知道该信道将仅用于传输股市行情数据,而不是神话故事或打油诗,这是完全合法的先验信息,通过以明确的方式限制样本空

间,它会对概率  $p_{i}$  产生明确的影响,尽管这可能很难用一般的数学术语来表述。

我们之所以强调这一点,是因为一些批评者对信息论不考虑语义的问题喋喋不休,认为这是我们整个哲学理念的一种基本缺陷,他们大错特错了:语义问题不是哲学理念问题,而是技术问题。我们不考虑语义的唯一原因是不知道如何将其作为一般流程来考虑,尽管对于特定有限的可能消息集合当然可以"人工"完成。所有人都可能试图利用自己对文本语义的感知来恢复一些毁坏的文本,但是我们如何教计算机做到这一点呢?

所以让我们向那些批评者保证:如果你能向我们提供一个确定可用的算法来评估语义,那么我们非常渴望将它也纳入信息论。事实上,我们目前无法做到这一点对于许多应用(从图像恢复到模式识别,再到人工智能)都是一种严重的障碍。我们需要你们的建设性帮助,而不是批评。

但是在传统的香农类型的通信理论中,唯一考虑的先验知识是"统计的",因为这可以立即进行数学处理。也就是说,它由过去类似信息样本中观察到的字母或字母组合的频率组成。一个典型的实际问题(实际上也是那些流行的文本压缩程序作者的实际问题)是,给定具有已知性质的可用信道如何设计编码系统,该系统将可靠地以最大可能的速率传输代表英文文本的二进制数字。这也是计算机硬件(如磁盘驱动器和调制解调器)的设计者的实际问题,只是变得更复杂一些。根据通常的观点,这时设计者需要给定正确的英文频率的准确数据。让我们考虑一下这个问题。

# 22.4 英语有统计性质吗?

假设为了研究通信理论,我们试图通过指定各种字母或字母组合的相对频率来表征英语。我们都知道,在诸如"字母E比Z出现的频率更高"这样的陈述中,有很多正确的成分。早在通信理论诞生之前,许多人就已经使用了这些常识。最早的例子是莫尔斯码的设计,其中最常用的字母由最短的代码表示——这是香农在一个世纪后形式化并精确化的通信理论的原型。

标准打字机键盘的设计充分利用了字母频率的知识。这一知识为奥特玛·梅根塔勒以更直接、极端的方式所使用,他的不朽语句

ETAOIN SHRDLU (22.25)

在Linotype排字机开始使用时经常在报纸上出现(一名没有经验的打字员,用手指在键盘上轻轻扫过时就会自动打出以上类型的语句)。但是我们已经遇到了麻烦,因为即使对于英语中12个最常见字母的相对顺序问题,似乎也没有完全一致的意见,更不用说它们相对频率值了。例如,根据普拉特(Pratt,1942),上

面的语句应该是

而特里布斯(Tribus,1961)给出的是

当涉及更低频使用的字母时,情况就变得更加混乱

当然,我们很容易看到产生这些差异的原因.获得不同英文字母相对频率值的人使用了不同的英文样本.很显然,百科全书的最后一卷会比第一卷具有更高的字母Z的相对频率.有机化学教科书、关于埃及历史的论文和现代美国小说中的词频会大不相同.受过高等教育的人与只有小学文化的人写出的东西在词频上会存在系统性差别.即使在更狭窄的领域内,我们也会预期詹姆斯·米切纳和欧内斯特·海明威著作中的字母和词频存在显著差异.从演讲录音中获取的字母频率很可能与演讲者写出的讲稿中的字母频率明显不同.

语言的统计性质因作者和环境而异的事实是显而易见的,以至于这已经成为一种有用的研究工具.詹姆斯·麦克多诺提交给哥伦比亚大学的一篇关于古典文学的博士论文中包含对荷马史诗《伊利亚特》的统计分析.古典研究者长期以来一直在争论:《伊利亚特》所有部分是否由同一个人撰写,以及荷马是否是一名真实的历史人物.分析表明,作品的整体风格是一致的.例如,15693行中有 $40.4\%$  以一个短音节后面跟两个长音节的单词结尾,这种单词结构从未出现在一行的中间.这种在希腊语中不太常见的特征的一致性似乎是表明《伊利亚特》是由一个人在相对较短的时间内写成的有力证据,而不是像一些19世纪的古典研究者所认为的那样是经过几个世纪演化的结果.

当然,演化论并不会被这个单一证据摧毁.如果唱《伊利亚特》,我们必须假设音乐具有原始音乐的非常单调的节奏模式,这种模式在很大程度上一直持续到巴赫和海顿.由于音乐的性质,作者可能已经强加了典型的文字模式.

考古学家告诉我们,《伊利亚特》中描述的特洛伊围城事件不是神话,而是发生在公元前1200年左右的一个历史事实.这大约比荷马的时代早1个世纪.米歇尔·文特里斯(Ventris & Chadwick,1956;Chadwick,1958;Ventris,1988)于1952年破译了米诺斯线性B文字,确定希腊语在特洛伊围城之前几个世纪就已经作为口语存在于爱琴海地区,但是排尼基字母的引人使得现代意义上的书面希腊语成为可能,这大约发生在荷马的时代.

以上两段仍然暗示演化在进行.显然,这个问题非常复杂,远没有被解决.但

是有意思的是,我们发现对单词和音节频率的统计分析代表在《伊利亚特》中存在了大约28个世纪的证据。对于任何行智慧提取它的人来说,它都最终被认为对这个问题的答案有明确的影响。

让我们回到通信理论,我们的观点很简单:说英文中存在且只存在一组"真实"字母或单词频率是完全错误的。如果我们使用以这种唯一定义频率存在为前提的数学模型,可能很容易证明一些东西,它们虽然作为数学定理完全有效,但对于实际设计通信系统以有效地传输英文的工程师来说,可能比无用还要糟糕。

但是假设我们的工程师确实有大量频率数据,而没有其他先验知识,他能如何利用这些信息来描述信息源呢?从我们提倡的角度来看,通信理论的许多标准结果可以被视为最大熵推断的简单例子,即与统计力学中相同类型的推断。

# 22.5 已知字频的最佳编码

假设我们的字母表由不同的符号  $A_{1}, A_{2}, \dots , A_{a}$  组成,用  $A_{i}, A_{j}$  等表示一般符号。任何由  $N$  个符号组成的消息都具有  $A_{i1}, A_{i2} \dots A_{iN}$  的形式。我们用  $M$  表示这一消息,它是指标集合的简写:  $M = \{i_{1}i_{2} \dots i_{N}\}$ 。可能的消息数为  $a^{N} \cdot \sum_{M}$  表示对它们进行求和。另外,我们定义

等等.

首先考虑工程师  $E_{1}$ ,他有一组数  $(f_{1}, \dots , f_{a})$ ,给出从历史消息样本中观察到的字母  $A_{j}$  的频率,但是没有其他先验知识。在只有这些信息的基础上,怎样的通信系统是合理的设计?为了以每秒  $n$  个符号的速率传输消息, $E_{1}$  需要多大的信道容量?

为了回答这个问题,我们需要有  $E_{1}$  分配给各种可能消息的概率分布  $p(M)$ 。现在, $E_{1}$  无法演绎地证明未来消息中的字母频率一定等于过去观察到的频率  $f_{i}$ 。另外,他的知识状态没有理由假设  $A_{i}$  的未来频率大于或小于  $f_{i}$ 。所以他将假设未来频率多少与过去相同,但是他不会对此过于武断。他可以要求分布  $p(M)$  只产生与过去已知频率相等的期望频率来做到这一点。换句话说,如果我们说分布  $p(M)$  "包含"某一信息,意思是该信息可以通过通常的估计方法从中提取出来。换句话说, $E_{1}$  将施加约束条件

$$
\langle N_{i} \rangle = \sum_{M} N_{i}(M) p(M) = N f_{i}, \quad i = 1, 2, \dots , a. \tag{22.29}
$$

当然, $p(M)$  不由这些约束条件唯一确定,因此  $E_{1}$  这时必须自由地选择某一分布。

我们再次强调,说这个问题中存在任何"物理"或"客观"概率分布  $p(M)$  是没有意义的。如果我们假设只有一条消息通过通信系统发送,无论这一消息是什么(也许我们知道通信系统随后将因木卫的影响而毁坏),我们都仍然希望它尽快并可靠地传输。因此,没有办法可以将  $p(M)$  确定为频率。但是这绝不会影响我们所考虑的工程设计问题。

在选择分布  $p(M)$  时,  $E_{1}$  完全可以假设一些涉及多个字母的消息结构。例如,他可以假设二元字母  $A_{1}A_{2}$  的可能性是  $A_{2}A_{3}$  的两倍。但是在  $E_{1}$  看来,这是不合理的,因为据他所知,基于任何此类假设的设计虽然可能带来好处,但同样可能有坏处。在  $E_{1}$  看来,理性保守的设计是小心地避免任何此类假设。简而言之,这意味着  $E_{1}$  应该选择与(22.29)一致的最大分布  $p(M)$ 。

现在,第11章中发展的最大摊断方法对于  $E_{1}$  是可用的。他的分布  $p(M)$  将具有形式

$$
\ln p(M) + \lambda_{0} + \lambda_{1}N_{1}(M) + \lambda_{2}N_{2}(M) + \dots +\lambda_{a}N_{a}(M) = 0, \tag{22.30}
$$

为了计算拉格朗日乘子  $\lambda_{i}$ ,他将使用分拆函数

$$
Z(\lambda_{1},\dots ,\lambda_{a}) = \sum_{M}\exp \left\{-\lambda_{1}N_{1}(M) - \dots -\lambda_{a}N_{a}(M)\right\} = z^{N}, \tag{22.31}
$$

其中

$$
z\equiv \mathrm{e}^{-\lambda_{1}} + \dots +\mathrm{e}^{-\lambda_{a}}. \tag{22.32}
$$

根据(22.29)以及一般关系

$$
\langle N_{1}\rangle = -\frac{\partial}{\partial\lambda_{i}}\ln Z(\lambda_{1},\dots ,\lambda_{a}), \tag{22.33}
$$

我们得到

$$
\lambda_{i} = -\ln (z f_{i}),\qquad 1\leqslant i\leqslant a. \tag{22.34}
$$

代回(22.30),我们得到描述  $E_{1}$  知识状态的分布是多项分布

$$
p(M) = f_{1}^{N_{1}}f_{2}^{N_{2}}\dots f_{a}^{N_{a}}. \tag{22.35}
$$

这是一个可交换序列,任何特定消息的概率仅依赖于字母  $A_{1},A_{2},\dots$  出现的次数,而不依赖于它们的出现次序。结果(22.35)是正确归一化的, $\sum_{M}p(M) = 1$ ,因为我们看到任何指定  $N_{i}$  的不同可能消息数是多项式系数

$$
\frac{N_{1}}{N_{1}!\cdots N_{a}!}. \tag{22.36}
$$

分布(22.35)的每个符号的确是

$$
H_{1} = -\frac{1}{N}\sum_{M}p(M)\ln p(M) = \frac{\ln Z}{N} +\sum_{i = 1}^{a}\lambda_{i}f_{i} = -\sum_{i = 1}^{a}f_{i}\ln f_{i}. \tag{22.37}
$$

在得到  $p(M)$  后,  $E_{1}$  可以通过香农(Shannon, 1948, 第9节)和法诺独立发现的方法以最有效的方式编码为二进制数字。将消息按概率递减的顺序排列,并通过分割将它们分成两类,使得分割左侧的所有消息的总概率尽可能地等于右侧消息的总概率。如果给定的消息属于左类,则其代码中的第1个二进制数字为0;如果属于右类,则为1。通过以尽可能接近1/4的总概率将这些类似地划分为子类,我们确定第2个二进制数字,等等。接下来请你证明(1)传输一个符号所需的二进制数字的期望数量等于  $H_{1}$  比特;(2)为了以每秒  $n$  个原始消息符号的速率传输,  $E_{1}$  需要信道容量  $C \geqslant n H_{1}$ ,这是香农首先给出的结果。

前面的数学步骤众所周知,以至于它们可能被认为微不足道。然而,我们给出的理论依据与常规处理的不同,这是本节的重点。传统上,人们会使用概率的频率定义,并说  $E_{1}$  的概率分配  $p(M)$  是假设不存在符号相互作用的结果。这种说法暗示假设可能正确或错误,并暗示如果要证明最终设计是合理的,就必须证明其正确性,即如果实际上存在  $E_{1}$  未知的符号相互作用,则所得到的编码规则可能不令人满意。

另外,我们认为概率分配(22.30)根本不是假设,而是不做假设。(22.30)表示:在某种朴素的意义上,是  $E_{1}$  除了指定期望的单字母频率外,完全不做任何假设,并且它是由该性质唯一确定的。因此,基于(22.30)的设计是  $E_{1}$  知识状态下最安全的设计。

我们的意思如下。事实上,如果  $E_{1}$  不知道的强符号间的相关性确实存在(例如Q总是跟在U之后),那么他的编码系统仍然能够很好地处理消息,无论这些相关性的性质如何。这就是我们说的,目前的设计是最保守的。它对相关性不做任何假设并不意味着它假设相关性不存在,如果相关性确实存在,就会遇到麻烦。相反,这意味着它为可能存在的任何类型的相关性提前做好了准备,它们不会导致性能下降。我们强调这一点是因为香农没有注意到这一点,而且这在最近的文献中似乎也没有被理解。

但是如果  $E_{1}$  得到了关于某种特定类型相关性的额外信息,他就可以使用它来设计一个新的编码系统,只要包含指定类型相关性的消息被传输,该系统将更加有效(即需要更小的信道容量)。但是,如果消息中的相关性突然发生变化,这种新的编码系统可能会变得比刚刚发现的更糟糕。

# 22.6 依据二元字母频率知识的更好编码

以下是一个相当长的数学推导,它在当前特定问题之外还有其他应用。考虑另一位工程师  $E_{2}$ 。他有一组代表二元字母  $A_{i} A_{j}$  的期望相对频率的信息  $f_{ij}$  (  $1 \leqslant$

$i \leqslant a, 1 \leqslant j \leqslant a$ .  $E_{2}$  将分配消息概率  $p(M)$  以与他的知识状态保持一致

$$
\langle N_{ij} \rangle = \sum_{M} N_{ij}(M) p(M) = (N - 1) f_{ij}, \tag{22.38}
$$

并且,为了避免任何进一步的假设,据他所知,这些假设可能会带来伤害,也可能会带来帮助,他将使用受这些约束的最大熵方法来确定消息  $p(M)$  的概率分布。如果他可以计算分拆函数

$$
Z(\lambda_{ij}) = \sum_{M} \exp \left\{-\sum_{i,j = 1}^{a} \lambda_{ij} N_{ij}(M) \right\} , \tag{22.39}
$$

问题就解决了。这可以通过解决给定  $\{N_{ij}\}$  的不同消息数量的组合问题来完成,或者观察到(22.39)可以写成以下矩阵乘积的形式:

$$
Z = \sum_{i,j = 1}^{a} \left(Q^{N - 1}\right)_{ij}, \tag{22.40}
$$

其中矩阵  $Q$  的定义如下:

$$
Q_{ij} \equiv \mathrm{e}^{-\lambda_{ij}}. \tag{22.41}
$$

如果假设消息  $A_{i_{1}} \dots A_{i_{N}}$  总是以第1个符号  $A_{i_{1}}$  结束,则它变成  $A_{i_{1}} \dots A_{i_{N}} A_{i_{1}}$  结果在形式上可以变得更简单。二元字母  $A_{i_{N}} A_{i_{1}}$  被添加到消息中,在(22.39)中会出现一个额外的因子  $\mathrm{e}^{- \lambda_{ij}}$ 。这样,修改后的分拆函数变成一个迹:

$$
Z' = \operatorname {Tr}\left(Q^{N}\right) = \sum_{k = 1}^{a} q_{k}^{N}, \tag{22.42}
$$

其中  $q_{k}$  是  $\left|Q_{ij} - q \delta_{ij}\right| = 0$  的根。物理学家将这种简化称为"使用周期性边界条件"。显然,这一修改不会导致长消息的极限有什么不同。当  $N \rightarrow +\infty$  时,

$$
\lim \frac{1}{N} \ln Z = \lim \frac{1}{N} \ln Z' = \ln q_{\max}, \tag{22.43}
$$

其中  $q_{\max}$  是  $Q$  的最大特征值。特定消息的概率现在是(22.40)的特例:

$$
p(M) = \frac{1}{Z} \exp \left\{-\sum \lambda_{ij} N_{ij}(M) \right\} , \tag{22.44}
$$

它产生(22.42)的特例的熵:

$$
S = -\sum_{M} p(M) \ln p(M) = \ln Z + \sum_{i,j} \lambda_{ij} \langle N_{ij} \rangle . \tag{22.45}
$$

鉴于(22.38)和(22.43),  $E_{2}$  的每个符号的熵在极限  $N \rightarrow +\infty$  时简化为

$$
H_{2} = \frac{S}{N} = \ln q_{\max} + \sum_{i,j} \lambda_{ij} f_{ij}, \tag{22.46}
$$

或者,由于  $\sum_{i,j} f_{ij} = 1$ ,我们可以将(22.46)写成

$$
H_{2} = \sum_{i,j} f_{ij} (\ln q_{\max} + \lambda_{ij}) = \sum_{i,j} f_{ij} \ln \frac{q_{\max}}{Q_{ij}}. \tag{22.47}
$$

因此,为了计算,我们不需要  $q_{\mathrm{max}}$  是  $\lambda_{ij}$  的函数(对于  $a \geq 3$ ,这在分析上是不切实际的),我们只需要找到作为  $f_{ij}$  函数的比率  $q_{\mathrm{max}} / Q_{ij}$ 。为此,首先引入矩阵  $Q$  的特征多项式:

$$
D(q) \equiv \operatorname {det}(Q_{ij} - q \delta_{ij}), \tag{22.48}
$$

并且注意到行列式的一些众所周知的性质,以供后面使用。第一个是

$$
D(q) \delta_{ik} = \sum_{j = 1}^{a} M_{ij} (Q_{kj} - q \delta_{kj}) = \sum_{j} M_{ij} Q_{kj} - q M_{ik}, \tag{22.49}
$$

以及类似的

$$
D(q) \delta_{ik} = \sum_{j} M_{jk} Q_{jk} - q M_{ki}, \tag{22.50}
$$

其中  $M_{ij}$  是行列式  $D(q)$  中  $Q_{ij} - q \delta_{ij}$  的余子式,即  $(- 1)^{i + j} M_{ij}$  是通过删除矩阵  $(Q_{kj} - q \delta_{kj})$  的第  $i$  行和第  $j$  列形成的矩阵的行列式。如果  $q$  是  $Q$  的任一特征值,则表达式(22.49)对于  $i$  和  $k$  的所有选择都将变为0。

第二个等式只在  $q$  是  $Q$  的特征值时成立。在这种情况下,矩阵  $M$  的所有余子式都为0。特别是,对于二阶余子式,

$$
D(q) = 0, \quad M_{ik} M_{jl} - M_{il} M_{jk} = 0. \tag{22.51}
$$

这表明比率  $M_{ik} / M_{jk}$  和  $M_{kl} / M_{kj}$  独立于  $k$ ,即  $M_{ij}$  一定具有形式

$$
D(q) = 0, \quad M_{ij} = a_{i} b_{j}. \tag{22.52}
$$

代入(22.49)和(22.52),表明  $b_{j}$  构成  $Q$  的右特征向量, $a_{i}$  构成左特征向量:

$$
\begin{array}{l}{{D(q)=0,\quad\sum_{j}Q_{k j}b_{j}=q b_{k},}}\\ {{D(q)=0,\quad\sum_{i}a_{i}Q_{i k}=a_{k}q.}}\end{array} \tag{22.53}
$$

现在假设  $Q$  的任一特征值  $q$  表示为拉格朗日乘子  $\lambda_{ij}$  的显式函数  $q(\lambda_{11}, \lambda_{12}, \dots , \lambda_{ua})$ ,那么在保持其他  $\lambda_{ij}$  不变时改变特定  $\lambda_{kl}$ , $q$  将变化以保持  $D(q)$  为0。根据行列式(22.48)的微分规则,得出

$$
\frac{\mathrm{d}D}{\mathrm{d}\lambda_{kj}} = \frac{\partial D}{\partial\lambda_{kl}} + \frac{\partial D}{\partial q} \frac{\partial q}{\partial\lambda_{kl}} = -M_{kl} Q_{kl} - \frac{\partial q}{\partial\lambda_{kl}} \operatorname {Tr}(M) = 0. \tag{22.55}
$$

使用这一关系,根据规定的二元字母频率  $f_{ij}$  固定拉格朗日乘子  $\lambda_{ij}$ ,条件(22.38)变为

$$
f_{ij} = -\frac{\partial}{\partial \lambda_{ij}} \ln q_{\mathrm{max}} = \frac{M_{ij} Q_{ij}}{q_{\mathrm{max}} \operatorname{Tr}(M)}. \tag{22.56}
$$

一元字母频率与  $M$  的对角元素成正比:

$$
f_{i} = \sum_{j = 1}^{a} f_{ij} = \frac{M_{ii}}{\operatorname{Tr}(M)}, \tag{22.57}
$$

这里使用了(22.49)在  $q = q_{\mathrm{max}}, i = k$  时为0的事实。因此,根据(22.56)和(22.57),计算每个符号的熵所需的比率是

$$
\frac{Q_{ij}}{q_{\mathrm{max}}} = \frac{f_{ij} M_{ii}}{f_{i} M_{ij}} = \frac{f_{ij} b_{i}}{f_{i} b_{j}}, \tag{22.58}
$$

其中我们使用了(22.52)。将其代入(22.47),我们发现涉及  $b_{i}$  和  $b_{j}$  的项抵消, $E_{2}$  的每个符号的熵就是

$$
H_{2} = -\sum_{i,j} f_{ij} \ln \frac{f_{ij}}{f_{i}} = -\sum_{i,j} f_{ij} \ln f_{ij} + \sum_{i} f_{i} \ln f_{i}. \tag{22.59}
$$

这绝不会大于  $E_{1}$  的  $H_{1}$ ,因为根据(22.42)和(22.59),

$$
H_{2} - H_{1} = \sum_{i,j} f_{ij} \ln \frac{f_{i} f_{j}}{f_{ij}} \leqslant \sum_{i,j} f_{ij} \left[ \frac{f_{i} f_{j}}{f_{ij}} - 1 \right] = 0, \tag{22.60}
$$

其中我们使用了当  $0 \leqslant x < +\infty$  时  $\ln x \leqslant x - 1$  的事实,当且仅当  $x = 1$  时等号成立。因此

$$
H_{2} \leqslant H_{1}, \tag{22.61}
$$

当且仅当  $f_{ij} = f_{i} f_{j}$  时等号成立,在这种情况下  $E_{2}$  的额外信息只是  $E_{1}$  会推断出的。要明白这一点,注意在消息  $M = \{i_{1} \dots i_{N} \}$  中,二元字母  $A_{i} A_{j}$  出现的次数为

\[ N_{ij}(M) = \delta(i, i_{1}) \delta(j, i_{2}) + \delta(i, i_{2}) \delta(j, i_{3}) + \cdots + \delta(i, i_{N- 1}) \delta(j, i_{N}), \] (22.62)如果我们让  $E_{1}$  通过最小化期望均方误差准则来估计二元字母  $A_{i} A_{j}$  的频率,他会做出估计

$$
\langle f_{ij} \rangle = \frac{\langle N_{ij} \rangle}{N - 1} = \frac{1}{N - 1} \sum_{M} p(M) N_{ij}(M) = f_{i} f_{j}, \tag{22.63}
$$

其中使用了  $E_{1}$  对于  $p(M)$  的分布(22.40)。事实上,如果  $f_{ij} = f_{i} f_{j}$ , $E_{1}$  和  $E_{2}$  得到的解是相同的,因为根据(22.56)(22.57)(22.52),我们有

$$
Q_{ij} = \mathrm{e}^{-\lambda_{ij}} = q_{\mathrm{max}} \sqrt{f_{i} f_{j}}. \tag{22.64}
$$

使用(22.43)(22.62)(22.64),我们发现  $E_{2}$  的分布(22.44)简化为(22.40)。这是我们在(11.93)中注意到的一个相当不平凡的例子。

# 22.7 与随机模型的关系

就以下问题而言,上面引入的量有着更深的含义。假设消息的一部分已经收到,那么  $E_{2}$  可以对消息的剩余部分说些什么呢?这可以通过诉诸我们的乘法规则

$$
p(AB|I) = p(A|BI) p(B|I) \tag{22.65}
$$

来回答,或者注意到给定  $B$  时  $A$  的条件概率是

$$
p(A|BI) = \frac{p(AB|I)}{p(B|I)}, \tag{22.66}
$$

在传统理论中从术提及先验信息  $I$  被引入到条件概率(即两个"绝对"概率的比率)的定义中.在我们的例子中,令  $I$  代表导致解(22.44)的问题的一般陈述且

那么  $p(AB|I)$  与(22.44)中的  $p(M)$  相同.使用(22.62),这简化为

$$
p(AB|I) = p(i_{1}\cdot \cdot \cdot i_{N}|I) = Z^{-1}Q_{i_{1}i_{1}i_{2}}Q_{i_{2}i_{3}\cdot \cdot \cdot \cdot Q_{i_{N}i_{1}i_{N}}}, \tag{22.69}
$$

且就像在分拆函数(22.40)中一样,在

$$
p(B|I) = \sum_{i_{m} = 1}^{a}\dots \sum_{i_{N} = 1}^{a}p(i_{1}\cdot \cdot \cdot i_{N}|I) \tag{22.70}
$$

中的和式生成矩阵  $Q$  的幂.为简洁起见,记  $i_{m - 1} = i,i_{m} = j,i_{N} = k$  且

$$
R\equiv \frac{1}{Z} Q_{i_{1}i_{2}}\cdot \cdot \cdot Q_{i_{m - 2}i_{m - 1}}, \tag{22.71}
$$

我们有

$$
P(B|I) = R\sum_{k = 1}^{a}\big(Q^{N + m + 1}\big)_{i k} = R\sum_{j,k = 1}^{a}Q_{i j}\big(Q^{N - m}\big)_{j k}, \tag{22.72}
$$

因此

$$
p(A|B I) = \frac{Q_{i j}Q_{i_{m}i_{m + 1}}\cdot\cdot\cdot Q_{i_{N - 1}i_{N}}}{\sum_{k = 1}^{a}\big(Q^{N - m + 1}\big)_{i k}}. \tag{22.73}
$$

由于包含在  $R$  中的所有  $Q$  相互抵消,我们看到消息的剩余部分  $\{i_{m}\dots i_{N}\}$  的概率仅取决于紧接在前面的符号  $A_{i}$  ,而不依赖于  $B$  的任何其他细节.这一性质定义了一个广义马尔可夫链.有大量文献涉及这个问题,这可能是概率论中得到最彻底解决的一个分支.在第3章中,我们在计算条件抽样分布时使用过它的一个基本形式.本质上所有其他内容都源于此的基本工具是"基础转移概率"矩阵  $(p_{i j})$  它是假设上一个符号是  $A_{i}$  ,下一个符号是  $A_{j}$  的概率  $p_{i j} = p(A_{j}|A_{i}I)$  .把(22.73)对  $i_{m + 1}\dots i_{N}$  求和,我们发现,对于长度为  $N$  的链,转移概率为

$$
p_{i j}^{(N)} = p(A_{j}|A_{i}I) = \frac{Q_{i j} - T_{j}}{\sum_{k}Q_{i k}T_{k}}, \tag{22.74}
$$

其中

$$
T_{j}\equiv \sum_{k = 1}^{a}\big(Q^{N - m}\big)_{j k}. \tag{22.75}
$$

$T_{j}$  依赖于  $N$  和  $m$  的事实是一个有趣的特征.通常,人们从一开始就考虑无限长的链,因此它仅是(22.74)在  $N\rightarrow +\infty$  时的极限,这是从未考虑过的.这个例子表明,链长的先验知识会影响转移概率.然而,极限情况显然是最令人感兴趣的.

为了得到极限,我们需要更多的矩阵理论.方程  $D(q) = \operatorname *{det}(Q_{i j} - q\delta_{i j}) = 0$  有根  $q_{1},q_{2},\dots ,q_{a}$  ,这些根不一定都不同且不一定都是实数.重新标记它们使得

$|q_{1}| \geqslant |q_{2}| \geqslant \dots \geqslant |q_{a}|$ . 存在一个非奇异矩阵  $A$  使得  $A Q A^{- 1}$  采用规范的"超对角"形式:

$$
A Q A^{-1} = \overline{{Q}} = \left( \begin{array}{c c c c c}{C_{1}} & 0 & 0 & \dots & 0\\ 0 & {C_{2}} & 0 & \dots & 0\\ 0 & 0 & {C_{3}} & \dots & 0\\ \vdots & \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & 0 & \dots & {C_{m}} \end{array} \right), \tag{22.76}
$$

其中  $C_{i}$  是具有以下形式之一的子矩阵:

$$
C_{i}=(\begin{array}{c c c c c c}{{q_{i}}}&{{1}}&{{0}}&{{0}}&{{\cdots}}&{{0}}\\ {{0}}&{{q_{i}}}&{{1}}&{{0}}&{{\cdots}}&{{0}}\\ {{0}}&{{0}}&{{q_{i}}}&{{1}}&{{\cdots}}&{{0}}\\ {{0}}&{{0}}&{{0}}&{{q_{i}}}&{{\cdots}}&{{0}}\\ {{\vdots}}&{{\vdots}}&{{\vdots}}&{{\ddots}}&{{\vdots}}\\ {{0}}&{{0}}&{{0}}&{{0}}&{{\cdots}}&{{q_{i}}}\end{array})\qquad\begin{array}{c c c c c c}{{(\begin{array}{c c c c c c}{{q_{i}}}&{{0}}&{{0}}&{{0}}&{{\cdots}}&{{0}}\\ {{0}}&{{q_{i}}}&{{0}}&{{0}}&{{\cdots}}&{{0}}\\ {{0}}&{{0}}&{{q_{i}}}&{{0}}&{{\cdots}}&{{0}}\\ {{0}}&{{0}}&{{0}}&{{q_{i}}}&{{\cdots}}&{{0}}\\ {{\vdots}}&{{\vdots}}&{{\vdots}}&{{\ddots}}&{{\vdots}}\\ {{0}}&{{0}}&{{0}}&{{0}}&{{\cdots}}&{{q_{i}}}\end{)}.}\end{array}). \tag{22.77}
$$

$Q$  的  $n$  次方是

$$
Q^{n} = A \overline{Q}^{n} A^{-1}, \tag{22.78}
$$

并且,当  $n \to +\infty$  时,从最大特征值  $q_{\mathrm{max}} = q_{1}$  产生的  $\overline{Q}^{n}$  的元素与所有其他元素相比会变得任意大.如果  $q_{1}$  是非退化的,它只出现在  $\overline{Q}$  的第1行和第1列,我们有

$$
\begin{array}{c}{{\lim _{N\rightarrow+\infty}\left[\frac{T_{j}}{q_{1}^{N-m}}\right]=A_{j1}\sum_{k=1}^{a}(A^{-1})_{1k},}}\\ {{\lim _{N\rightarrow+\infty}\left[\frac{T_{j}}{\sum_{k}Q_{i k}T_{k}}\right]=\frac{A_{j1}}{q_{1}A_{i1}}.}}\end{array} \tag{22.80}
$$

极限转移概率是

$$
p_{i j}^{(\infty)} = \frac{Q_{i j}}{q_{1}}\frac{A_{j1}}{A_{i1}} = \frac{Q_{i j}}{q_{1}}\frac{M_{i j}}{M_{i i}}, \tag{22.81}
$$

其中我们使用了一个事实,即  $Q$  的特征向量中的元素  $A_{j1}$ $(j = 1,2,\dots ,a)$  具有特征值  $q_{1} = q_{\mathrm{max}}$  因此,参考(22.52)有  $A_{j1} = K b_{j}$ ,其中  $K$  是某个常数.使用(22.56)和(22.57),我们最终有

$$
p_{i j}^{(\infty)} = \frac{f_{i j}}{f_{i}}. \tag{22.82}
$$

从这个很长的计算过程中,我们学到了很多东西.首先,对于有限长度的序列(实际存在的唯一类型),精确解具有依赖于长度的精细结构.当然,那些试图在问题

开始时直接跳入无限集合的人是学不到这一点的。其次, 有趣的是标准矩阵理论足以完全解决这个问题。最后, 在无限长序列的极限下, 最大熵问题的精确解确实进入了我们熟悉的马尔可夫链理论。这让我们可以更深入地了解马尔可夫链分析的基础及其可能的局限性。

练习22.1 最后一句的确切含义可能不清楚。在经典马尔可夫链中, 两步的转移概率由一步矩阵  $(p_{ij})$  的平方给出, 三步的转移概率由该矩阵的立方给出, 依此类推。但是我们的解是对相应的指标求和 (22.73) 来确定多步概率, 这显然不是一回事。对此进行研究并确定最大熵多步概率是否与经典马尔可夫概率相同, 或者它们是否在某些极限下变得相同。

我们看到最大熵原理足以确定无噪声通道最佳编码问题的显式解。当然, 当我们考虑更复杂的约束 (如三元字母频率等) 时, 用笔纸来求解将变得无比困难 (对此没有"标准矩阵理论"), 据我们所知, 这必须求助于计算机求解。

现在, 香农号称最强的定理涉及给定  $n$  元字母频率在  $n \rightarrow +\infty$  极限的问题。他的  $H \equiv \lim H_{n}$  被认为是英语的"真实"熵, 决定了传输它所需的"真实"最小信道容量。我们不怀疑这是一个有效的数学定理, 但是从以上讨论中可以清楚地看出, 这样的定理与现实世界无关, 因为即使是在  $n = 1$  时, 英语也不存在"真实"的  $n$  元字母频率这样的东西。

事实上, 就算这样的频率确实存在, 也请想一想人们如何确定它们。即使我们不区分大小写字母, 也不在字母表中包含十进制数字或标点符号, 但是仍有  $26^{10} = 1.41 \times 10^{14}$  个 10 元字母频率需要测量和记录。要以每张纸 1000 条的方式将它们全部存储在纸上, 需要一叠大约 11300 千米厚的纸。

# 22.8 噪声通道

让我们研究最简单的非平凡情况, 其中噪声独立 (无记忆地) 作用于每个传输的字母。假设每个字母独立地具有被错误传送的概率  $\epsilon$ , 那么在  $N$  个字母的消息中, 有  $r$  个错误的概率是二项分布

$$
p(r)={\binom{N}{r}}\epsilon^{r}(1-\epsilon)^{N-r}, \tag{22.83}
$$

并且期望错误数是  $\langle r \rangle = N \epsilon$ 。如果  $N \epsilon \ll 1$ , 我们可以认为该通信系统对大多数用途是令人满意的。然而, 信息的传输可能必须完全没有任何错误 (如向在轨卫星发送计算机代码指令)。纠错码领域已经有大量文献和许多复杂的理论, 但是一个非常流行与简单的流程是使用校验和。

正如计算机实践中通常的情况, 假设我们的"字母表"由  $2^{8} = 256$  个不同的字符组成. 每个字符以 8 位二进制数发送, 称为"字节". 在消息的末尾, 再传输 1 字节, 它在数值上是前  $N$  字节的和 (mod 256). 接收器根据接收到的前  $N$  字节重新计算该和, 并将其与传输的校验和进行比较. 如果它们一致, 那么几乎可以肯定传输没有错误 (如果有错误, 那么一定至少有两个错误恰好在校验和中相互抵消, 这种概率极其小, 远小于  $\epsilon$ ). 如果它们不一致, 那么肯定有传输错误, 因此接收器向发送器发送"请重复"信号, 并重复该过程, 直到实现无差错传输.

让我们看看根据概率论, 校验和流程有多好. 为简洁起见, 记

$$
q \equiv (1 - \epsilon)^{N + 1}. \tag{22.84}
$$

然后, 为了实现无差错传输, 我们有

概率  $q$  需要传输  $N + 1$  个符号,

概率  $(1 - q)q$  需要传输  $2(N + 1)$  个符号,

概率  $(1 - q)^{2}q$  需要传输  $3(N + 1)$  个符号,

等等.

实现无差错传输的期望传输长度是

$$
\langle N\rangle = (N + 1)q[1 + 2(1 - q) + 3(1 - q)^{2} + 4(1 - q)^{3} + \dots ]. \tag{22.85}
$$

由于  $|1 - q| < 1$ , 级数收敛到  $1 / q^{2}$ , 所以

$$
\langle N\rangle = \frac{N + 1}{(1 - \epsilon)^{N + 1}} \simeq N \mathrm{e}^{N \epsilon}, \tag{22.86}
$$

如果  $N \gg 1$ , 则近似值保持得相当好. 但如果消息太长以至于  $N \epsilon \gg 1$ , 则此流程失效. 我们几乎不可能在可接受的时间内无误地传输它.

但是现在我们有一个巧妙的方法来挽救, 它表明一点儿概率论如何可以帮助我们达到准确传输. 让我们将长消息分成  $m$  个较短的、长度为  $n = N / m$  的块, 并使用自己的校验和传输每一块. 根据 (22.86), 期望的总传输长度现在是

$$
\langle L\rangle = m \frac{n + 1}{(1 - \epsilon)^{n + 1}} = N \frac{n + 1}{n(1 - \epsilon)^{n + 1}}. \tag{22.87}
$$

很明显, 如果块太长, 那么我们将不得不重复多次; 如果块太短, 那么我们将浪费传输时间发送许多不必要的校验和. 因此, 应该有一个使 (22.87) 最小的最优块长度. 顺理成章地, 结果证明这与  $N$  无关. 改变  $n$ , 当

$$
1 + n(n + 1) \ln (1 - \epsilon) = 0, \quad \text{或} \quad (1 - \epsilon)^{n + 1} = \mathrm{e}^{-1 / n} \tag{22.88}
$$

时 (22.87) 达到最小值. 对于所有实际目的, 最优块长度是

$$
(n)_{\mathrm{opt}} = \frac{1}{\sqrt{\epsilon}}, \tag{22.89}
$$

最小可达到的期望长度是

$$
\langle L\rangle_{\min} = N\left(\frac{n + 1}{n}\right)\exp \left\{\frac{1}{n}\right\} \simeq N(1 + 2\sqrt{\epsilon}). \tag{22.90}
$$

通过将长消息分成多块,我们取得了巨大的进步.如果  $\epsilon \simeq 10^{- 4}$  ,则通过单块发送长度为  $N = 100000$  字节的无错误消息是不切实际的,因为在每次传输中预计大约有10个错误,预期的传输长度约为  $22000N$  字节,这意味着我们平均必须重复约22000次才能得到无错误的结果,但是最优块长度约为  $n\simeq 100$  ,通过使用它,期望长度减少到  $\langle L\rangle = 1.020N$  ,这意味着我们需要发送1000个块,其中每个块都有额外的1字节(这大致相当于因子  $(n + 1) / n\simeq 1 + \sqrt{\epsilon})$  ,大约10个可能需要重复(对应于因子  $\mathrm{e}^{1 / n}\simeq 1 + \sqrt{\epsilon})$  ,但是(22.87)中的最小值非常宽:如果  $40\leqslant n\leqslant 250$  ,我们有  $\langle L\rangle \leqslant 1.030N$  ,如果  $\epsilon = 10^{- 6}$  ,则分块方法允许我们传输任何长度的无差错消息,而且几乎没有传输时间的损失(如果  $n$  接近1000,则  $\langle L\rangle \simeq 1.002N$  )

据我们所知,分块方法是一种基于直觉的特定工具,不是从任何最优性准则中衍生出来的,但是它使用起来很简单,并且非常接近所希望的最好值(  $\langle L\rangle = N$  ),因此几乎没有任何动力去寻找更好的方法.

在微型计算机的早期,消息以128字节或256字节的块长度进出磁盘,如果每字节的错误概率在  $\epsilon \simeq 10^{- 5}$  的数量级,这将是最优的.在撰写本文时(1991年),消息改为以1024字节到4096字节的块发送,这表明现在磁盘读写对于数量级为 $10^{- 8}$  或更小的错误概率是可靠的.当然,保守的设计使用的块长度比上述最优值略短,以防止设备磨损和错误率增加导致性能下降.

但是让我们注意一个哲学观点,在这个讨论中,我们是否已经放弃作为逻辑的概率论的立场,而回到了频率定义?一点儿也不!如果错误概率  $\epsilon$  确实是在所有重复类别测量中的"客观真实"错误频率,那么我们的  $\langle L\rangle_{\min}$  同样是在同样类型重复的客观真实的最小可达到的平均传输长度,这是完全正确的.

但在只有在极少数情况下,这才是真实情况.这类实验很耗费时间和资源.在现实世界中,在设计截止并将制造产品交付给客户之前,它们永远不会完成.事实上,在高可靠系统上的可靠性实验永远不可能真正完成,因为在需要进行的时候,我们的知识状态和技术能力会发生变化,使得基于最初目标的测试变得无关紧要.

我们现在的观点是,无论我们的概率是否为真实频率,作为逻辑的概率论在如下意义上都有效,正如我们在第8章中看到的,作为逻辑的概率论的一个可推导的基础结果是,我们的概率是我们可以对所拥有信息做出的频率的最优估计.

这样, 无论概率分配  $\epsilon$  所依据的证据是什么, 上述方程都描述了此时此地根据我们所掌握的信息可以做出的最合理的设计. 如前所述, 即使事先知道只有一条消息将通过我们的通信系统发送, 这仍然是正确的. 因此, 作为逻辑的概率论具有更广泛的应用, 即使有人有时出于心理原因假装自己使用频率定义时也是如此.

# 附录A 概率论的其他流派

毋庸置疑,我们在第2章中构建概率论的方式并不是唯一的。我们所选择的特定条件可能有其他选择方式,而且还有其他几种基于完全不同概念的流派。

对于前者,许多定性陈述似乎很显然,以至于人们可能会认为它们才是基本公理或合情条件,而不是我们所使用的那些。因此,如果  $A$  蕴涵  $B$ ,那么对于所有  $C$ ,我们直觉上应该期望  $P(A|C) \leqslant P(B|C)$ 。当然,我们的规则确实具有这个性质,因为乘法规则是

$$
P(AB|C) = P(B|AC)P(A|C) = P(A|BC)P(B|C). \tag{A.1}
$$

如果  $A$  蕴涵  $B$ ,那么  $P(B|AC) = 1$  且  $P(A|BC) \leqslant 1$ ,因此乘法规则会简化为直觉的结论。选择不同的公理很可能会简化第2章的推导。然而,这不是我们使用的标准。我们选择在我们看来最原始且最无可争辩的命题作为起点,相信由此产生的理论将具有可能的最大普遍性和应用范围。

下面简要地说明一些过去的其他流派。

# A.1 柯尔莫哥洛夫概率系统

在第2章末尾的评注中,我们注意到维恩图以及它与集合论的关系,这成为柯尔莫哥洛夫概率论方法的基础。这种方法在一般视角与动机上与我们的有很大不同,但是最终结果与我们的方法在几个方面是相同的。

柯尔莫哥洛夫概率系统(此后用KSP表示)是在基本命题  $\omega_{i}$  (或"事件",在这个抽象层次上我们称之为什么无关紧要)的样本空间  $\Omega$  上玩的游戏。尽管抽样定义没有这么说明,我们可以认为它们大致对应于维恩图上的各个点。

然后存在一个域  $F$  由选定的  $\Omega$  上的子集  $f_{j}$  组成。这大致对应于我们的命题  $A, \ldots , B, \ldots$ ,由维恩图的区域表示(尽管抽象定义让集合不需要对应于区域)。 $F$  具有三个基本性质。

(I)  $\Omega$  在  $F$  中。

(II)  $F$  是一个  $\sigma$  域,意思是如果  $f_{j}$  在  $F$  中,那么它关于  $\Omega$  的补  $\overline{f}_{j} = \Omega - f_{j}$  也在  $F$  中。

(III)  $F$  对于可数并是封闭的,这意味着,如果可数个  $f_{j}$  在  $F$  中,它们的并也在  $F$  中。

最后,在  $F$  上存在具有以下性质的概率测度  $P$ .

(1)归一化:  $P(\Omega) = 1$

(2)非负性:对于  $F$  中的所有  $f_{i}$  有  $P(f_{i}) \geqslant 0$

(3)可知性:如果  $\{f_{1},\dots ,f_{n}\}$  是  $F$  中的不相交元素(即它们没有共同点  $\omega_{i}$  ),则  $P(f) = \sum_{i}P(f_{i})$  ,其中  $f = \bigcup_{j}f_{j}$  是它们的并.

(4)零连续性:如果序列  $f_{1} \supseteq f_{2} \supseteq f_{3} \supseteq \dots$  趋于空集,则  $P(f_{j}) \to 0$  这些公理没有什么令人惊讶的地方. 它们似乎是我们在第2章中所发现的熟悉内容,只是陈述了集合而不是命题的类似性质.

对于任何能被证实也能被证否的命题,柯尔莫哥洛夫想要  $F$  是一个  $\sigma$  域,这与我们在精神上是一致的. NOT运算也是我们的原始运算之一. 事实上,我们通过包含AND运算走得更远. 令人惊喜的是,(AND, NOT)是演绎逻辑的完备集合,结果证明对于我们的扩展逻辑也是完备的(即给定一组待考虑的命题  $\{A_{1},\dots ,A_{n}\}$  ,我们的规则生成了一个形式上完全的推理系统,因为它足以为  $\{A_{1},\dots ,A_{n}\}$  通过布尔代数生成的所有命题分配一致的概率.)

在以下意义上,这一要求也暗示了柯尔莫哥洛夫在可列并下的闭包. 从根本上使用有限集合,我们从根本上满足于有限并;然而,作为有限集合良好定义极限的无限集合可能是一种方便的简化,可以为有限集合计算去除复杂但不相关的细节. 在如此产生的无限集合上,我们的有限并进入可数并.

但是,正如第2章中所指出的,一个涉及现实世界的命题  $A$  不是总能被视为有意义的集合  $\Omega$  的基本命题  $\omega_{i}$  的析取(或),而它的否  $\overline{A}$  可能更难以解释为集合的补. 试图将命题  $A, B, \dots$  上的逻辑运算替换为集合上的集合操作不会改变理论的抽象结构,却使得它在应用中可能重要的方面变得不那么一般. 因此,我们试图在作为亚里士多德逻辑的扩展的更广泛意义上来构建概率论.

最后,柯尔莫哥洛夫将概率测度  $P$  的性质  $(1) \sim (4)$  表述为看似随意的公理,而KSP因为这种随意性而受到批评. 但是,我们认为它们只是对我们在第2章中根据一致性需求导出的四个性质在集合场景中的陈述. 例如,从(2.35)可以明显看出对非负性的需求. 仅作为公理表述时,可加性似乎也是随意的,但是在(2.85)中,我们根据一致性的需要推导出了它.

许多人认为归一化只是一种随意的约定,但(2.31)表明,如果确定性不用  $p = 1$  表示,那么我们必须重述加法规则和乘法规则,否则就会出现不一致. 例如,如果我们选择  $p = 100$  来表示确定性的约定,那么这些规则的形式为

$$
p(A|B) + p(\overline{A} |B) = 100, \quad p(A|BC)p(B|C) = 100p(AB|C). \tag{A.2}
$$

更一般地,通过变量  $u = f(p)$  对某个单调函数  $f(p)$  的变换,我们可以在不同的尺度上表示概率,但是一致性将要求乘法规则和加法规则在形式上也进行修改以使得我们的理论内容不会改变。例如,对于  $u = \ln [p / (1 - p)]$  的变换,加法规则采用同样简单的形式

$$
u(A|B) + u(\overline{A} |B) = 0, \tag{A.3}
$$

而乘法规则将变得非常复杂。实质性的结果并不是人们必须使用任何特定尺度,而是其中有一个归一化、非负可加的唯一尺度的内容不同的概率论将会包含不一致性。

这应该可以回答某些人(Fine,1973,第65页)提出的反对意见,即柯尔莫哥洛夫的尺度是任意的。在1973年,这样指责看起来似乎是合理的,需要进一步研究。根据进一步的研究,我们现在知道,他实际上做出了唯一能够通过我们所有一致性检验的选择,现在我们认为这种指责是不合理的。

我们不知道柯尔莫哥洛夫是如何看到其公理(4)(零连续性)的必要性的,但是我们的方法实际上可以根据简单的一致性要求来导出它。首先,让我们消除一种误解。关于集合的陈述(4)似乎暗示给定了一个无限的子集序列,但是将其解释成关于命题的陈述并不要求我们将概率分配给无限数量的命题。重要的是,我们拥有无限序列的不同知识状态,这可能是关于一个单一命题的,但是趋于不可能。由于柯尔莫哥洛夫的集合与任何诸如"知识状态"之类的思想无关,因此在集合场景中似乎无法这样说,但在命题场景中,这很容易。

我们写下这一点是为了强调,"通过将讨论限制在一组有限命题上就可以不需要这一公理"是一个严重的错误。由此产生的理论将使得人们很容易犯各种不一致错误。

在我们的系统中,"零连续性"采用以下形式:给定一系列趋于确定性的概率  $p(A)_1, p(A)_2, \dots$  ,分配给相应否定的概率  $p(\overline{A})_1, p(\overline{A})_2, \dots$  一定趋于零。事实上,正如我们在(2.48)中所指出的那样, $S(x)$  满足的函数方程使得不同  $x$  值之间的联系非常紧密,以至于当  $x \to 1$  时  $S(x)$  趋于0的确切方式在整个值域(  $0 \leqslant x \leqslant 1$  )中决定函数  $S(x)$ ,因此决定可加性(2.58)。因此,从我们的角度来看,柯尔莫哥洛夫公理(3)和(4)似乎是密切相关的,它们在逻辑上是否独立并不显而易见。

因此,出于所有实际目的,如果将概率论应用于集合论场景,我们的系统将与KSP一致。但是在更一般的应用中,虽然我们有一个具有相同性质的话语域  $F$  和  $F$  上的概率测度  $P$ ,但是我们不需要,也不总是有  $F$  中的元素都可以分解成的基本命题集合。当然,在我们的许多应用中会出现这样一个集合:例如,在平衡统计力学中, $\Omega$  中的元素  $\omega_i$  可以用系统平稳"全局"量子态来识别,它形成一

个可数集合. 在这些情况下, 抽象理论阐述基本上会完全一致, 尽管出于以下原因, 我们在实际计算中一方面有更多自由, 而另一方面则有更多禁忌.

我们的方法也以另一种方式支持 KSP. KSP 被批评为缺乏与现实世界的联系. 在某些人看来它的公理是有缺陷的, 因为它们不包含任何测度  $P$  在实际问题中能解释为随机试验的频率的陈述. 但是在我们看来, 这似乎是优点而不是缺陷. 要求我们在使用概率论之前援引某个随机试验会对理论的适用范围施加不可容忍的随意的限制, 使得概率论不适用于我们建议通过扩展逻辑解决的大多数问题.

即使在实际问题中援引了随机试验, 适当考虑了指定频率的命题, 这也不是用来确定测度  $P$  的, 而是作为域  $F$  的元素. 在柯尔莫哥洛夫的系统和我们的系统中, 这样的命题不是进行推断的工具, 而是进行推断的事物.

然而, 这两种概率论体系之间存在一些重要差别. 首先, 在 KSP 中注意力几乎完全集中在可加测度的概念上. 柯尔莫哥洛夫公理没有提到条件概率的概念. 事实上, KSP 认为这是一个实际上不需要的尴尬概念, 只是在看似重新考虑后不情愿地提到它. 尽管柯尔莫哥洛夫的书中有一节名为"贝叶斯定理", 但是他的大多数跟随者忽略了它. 相比之下, 我们从一开始就认为, 所有涉及现实世界的概率都必须以当前所掌握的信息为条件. 在第 2 章中, 乘法规则——条件概率和贝叶斯定理是其直接结果——甚至在可加性之前就出现在我们的系统中.

我们的推导表明, 从逻辑的角度来看, 乘法规则 (以及贝叶斯定理) 简单地表达了布尔代数的结合性和交换性. 这是我们在计算中拥有更多自由的原因, 使得我们在后面的章节中不受限制地使用贝叶斯定理. 在该定理中, 我们可以完全自由地以乘法规则和加法规则允许的方式在任何概率符号的左右两侧来回移动命题. 这是一个极好的计算工具, 也是迄今为止最强大的科学推断工具, 但它完全没有出现在基于 KSP 工作的概率论阐述中 (它根本不将概率论与信息或推断联系起来).

作为对这种自由的回报, 我们对自己施加了 KSP 中不存在的一种限制. 在被德菲内蒂和他的追随者抨击之后, 我们对无限集合保持警惕. 我们只在确保问题中存在一个明确定义且行为良好的极限过程, 不会导致我们陷入悖论且有用时才会使用它.

原则上, 我们总是从枚举一些有限的命题  $A, B, \dots$  开始. 因此, 我们的话语域  $F$  也是有限的, 它由这些命题以及可以通过合取 (交、与)、析取 (并、或)

和否定从中自动“构建”的所有命题组成。我们没有必要，也不希望将它们分解为更细命题的析取，更不用说将其扩展到无穷极限了，除非由于特定问题的结构，这可能成为一种有用的计算工具。

我们采取这种立场有三个原因．第一个原因在第8 章中通过萨姆的坏温度计场景进行了说明，我们看到超过某个点之后，这种越来越细的分解毫无意义．第二个原因是，在第15 章中，我们看到一些悖论在等待着那些不考虑有限集合的任何极限过程，而直接跳入无限集合的人．但是即使在这里，当我们考虑所谓的“博雷尔- 柯尔莫哥洛夫悖论”时，也发现自己同意柯尔莫哥洛夫对它的解决方案，而不同意他的一些批评者的意见．我们必须小心地处理无限集合，但是一旦进入不可数集合，也必须同样小心地处理测度为0 的集合

第三个原因是，不同的分解方式通常对我们更有用．除了将命题  $A$  分解为“较小” 命题的析取  $A = B_{1} + B_{2} + \dots$  并应用加法规则外，我们同样可以将其分解为“较大” 命题的合取  $A = C_{1}C_{2}\dots$  并应用乘法规则．这可以非常简单地以集合术语解释．要确定一个国家的地理布局，有两种可能的方法：(1) 指定其中的点；(2) 指定其边界．方法(1) 是维恩- 柯尔莫哥洛夫的方法，但是在我们看来，方法(2) 同样基本，而且通常更简单，并与我们在实际问题中所拥有的信息更直接相关．在维恩图中，集合  $A$  的边界由  $C_{1},C_{2},\dots$  的边界组成，正如一个国家的边界是由河流、海岸线和相邻国家组成的一样

这些方法并不冲突，在每一个问题中，我们都可以选择恰当的方法．但是在大多数问题中，方法(2) 是更自然的．物理理论总是被表述为假设的合取，而不是析取；同样，数学理论是由它背后的一组公理定义的，它总是被表述为基本公理的合取．将任何理论的基础表述为析取几乎是不可能的，因此我们必定需要这种选择的自由

总之，到目前为止，看不到我们的概率系统与柯尔莫哥洛夫系统之间有任何实质性冲突．但是，我们寻求更深层次的概念基础，使其能够扩展到更广泛的应用类型，这是当前科学问题所需要的

然而，这里阐述的理论还远未达到其最终完整的形式．在目前的发展状态下，在很多情况下，我们的机器人不知道如何处理它的信息．假设有人告诉它“琼斯对  $\theta$  可能大于100 的提示感到非常高兴”，那么通过什么原则可以将其转化为关于  $\theta$  的概率陈述呢？

然而，我们可以利用这些信息来修改我们对  $\theta$  的看法（根据我们对琼斯的看法向上或向下调整）．事实上，我们几乎可以使用任何类型的先验信息，也许可以绘制一条曲线，粗略地表明它如何影响我们的概率分布  $p(\theta)$  ．换句话说，我们的

大脑掌握着比机器人更多的原理,可以半定量地将原始信息转换为计算机可以使用的东西。这就是为什么我们坚信一定有更多的诸如最大熵和变换群之类的原理等着被人发现。每一个这样的发现都将为这一理论的应用开辟一个新的领域。

# A.2 德菲内蒂概率系统

现在有一个活跃的概率学派,他们的大多数成员称自己为"贝叶斯主义者",但是实际上是布鲁诺·德菲内蒂的追随者,关心的是贝叶斯从未想过的事情。1937年,德菲内蒂发表了一部作品,该作品表达了一种与我们有些相似的哲学,不仅包含他奇妙而核心的可交换性定理,而且试图在"连贯性"概念上建立概率论本身的基础。这大致意味着,人们应该以在基于概率的投注中不会肯定成为输家的原则分配和操作概率。他(de Finetti, 1937)似乎很容易地从这个前提中推导出了概率论的规则。

自1937年以来,德菲内蒂发表了更多关于该主题的著作(de Finetti, 1958, 1974a,b)。请特别注意以英文翻译出版的大型著作(de Finetti, 1974b)。有些人认为我们应该在当前工作中遵循德菲内蒂的连贯性原则。当然,那会缩短我们的推导过程。但是,我们认为连贯性在三个方面都不是令人满意的基础。第一个无疑只是美学上的,在我们看来,将逻辑原则建立在诸如期望利润这样粗俗的事情上是不优雅的。

第二个方面是策略上的。如果认为概率从根本上是根据投注偏好来定义的,那么分配概率时人们的注意力就集中在如何诉诸不同人的个人概率上。在我们看来,这是一项有价值的努力,但是属于心理学领域而不是概率论领域,我们的机器人没有任何投注偏好。当我们以作为逻辑的规范扩展应用概率论时,我们关心的不是不同人可能碰巧拥有的个人概率,而是考虑到他们所拥有的信息时所"应该"拥有的概率——正如詹姆斯·克拉克·麦克斯韦在第1章章首引文中指出的那样。

换句话说,从问题一开始,我们关心的就不是任何人的个人意见,而是在当前问题的背景下如何指定先验信息,这些先验信息是我们机器人意见的基础。通过对先验信息的逻辑分析来一致地分配先验概率的原则对我们来说是概率论的必要组成部分。在基于德菲内蒂方法的概率论阐述中几乎完全没有考虑这一点(当然它并不禁止我们考虑此类问题)。

第三个方面完全是实用的:如果发现任何规则具有德菲内蒂意义上的连贯性,但不具有考克斯意义上的一致性,那么作为逻辑推断的规则,它显然是不可接受的——实际上,在功能上是不可用的。不会有"正确方式"来做任何计算,任何

问题也都没有"正确答案". 然后想想所有这些不同的答案至少是"连贯的", 这会让人感到些许安慰.

据我们所知, 德菲内蒂没有将一致性作为一种合情条件提及, 也没有对其进行检验. 然而, 一致性——而不仅仅是连贯性——才是必不可少的. 我们发现, 当我们指定的规则满足一致性要求时, 它们很容易自动具有连贯性.

我们在前言中还提到了另一点. 与柯尔莫哥洛夫一样, 德菲内蒂主要关注在任意不可数集上直接定义的概率, 但是他以不同的方式看待可加性, 并且导致了像洋葱一样无限层序列的异常情况, 不同阶数 0 概率相加起来等于 1 , 等等. 德菲内蒂的追随者犯下了大部分无限集合悖论迫使我们转向 (并且就像第 16 章中的亥姆霍兹那样在必要时夸大) 相反的"有限集合"策略以避免它们. 这一思想及其技术细节在第 15 章中有所陈述.

# A.3 比较概率

在 1.8 节中, 我们注意到有人可能会反对我们的第一个合情条件:

(I) 合情性应由实数表示.

为什么这个条件必要? 一个现实的理由是: 除非在某一点, 合情性与某个确定的物理量相关联, 我们无法明白机器人的大脑如何通过执行确定的机械或电子物理操作来发挥作用.

我们认识到这缺乏一些美感 (忽略了一些美学上的考虑). 例如, 欧几里得几何之所以优雅. 很大程度上是因为它不关心数值, 而只认等价或相似的定性条件. 在选择其他公理时, 我们非常注意这一点, 小心确保"一致性"和"符合常识"表达的是定性而不是定量性质.

当然, 我们基于现实的论证对于那些关心抽象公理而不关心实效的人没有任何意义, 所以让我们考虑替代方案. 如果有人想替换我们的合情条件 (I), 可以将其分解为更简单的公理. 在下文中, " $(A|C) > (B|C)$ " 不是指数字比较, 而只是"给定  $C$ ,  $A$  比  $B$  更合情"的文字表达, 等等. 那么合情条件 (I) 可替换为两个更基本的条件.

(Ia) 传递性. 如果  $(A|X) \geqslant (B|X)$  且  $(B|X) \geqslant (C|X)$ , 则  $(A|X) \geqslant (C|X)$ .

(Ib) 普遍可比性. 给定命题  $A, B, C$ , 那么关系  $(A|C) > (B|C)$ ,  $(A|C) = (B|C)$ ,  $(A|C) < (B|C)$  其中之一必须成立.

要明白这一点, 注意如果同时假定传递性与普遍可比性成立, 那么对于任何有限命题集合, 我们总是可以建立服从所有排序关系的实数 (实际上是有理数)

的表示. 因为, 假设有一个具有数值度量  $\{x_{1}, \dots , x_{n}\}$  的命题集合  $\{A_{1}, \dots , A_{n}\}$ , 添加一个新命题  $A_{n + 1}$ , 传递性与普遍可比性确保它会在符合这些排序关系时具有唯一位置. 由于任何两个有理数之间总能找到另一个有理数, 我们总是可以给它分配一个数  $x_{n + 1}$  使得有理数  $\{x_{1}, \dots , x_{n + 1}\}$  也服从新集合  $\{A_{1}, \dots , A_{n + 1}\}$  的排序关系.

所有体现传递性和普遍可比性的比较理论至此完结. 一旦建立了实数表示的存在性, 考克斯定理就会生效并使得该理论与我们在第 2 章中推导出的理论相同. 也就是说, 要么存在某一单调函数服从概率论的标准乘法规则和加法规则, 要么我们可以展示在比较理论的规则中存在不一致性.

一些比较概率论系统同时具有这两个公理, 这样它们就假设了保证与标准数值理论等价所需的一切. 在这种情况下, 拒绝使用数值表示的极大便利似乎是愚蠢的. 但是现在, 是否可以放弃传递性或普遍可比性, 并获得与我们内容不同的、可接受的扩展逻辑理论?

如果违反传递性, 比较概率论就不会走得太远. 没有人愿意或者能够使用它, 因为我们会陷入无限的循环推理. 所以, 传递性肯定会成为比较概率论的公理之一, 发现不可传递性将成为立即拒绝任何理论系统的理由.

对许多人来说, 普遍可比性似乎并不是一个令人信服的合情条件. 去掉它, 我们可以创建一种"网格"理论. 之所以这么叫, 是因为我们可以用点来表示命题, 用通过各种方式连接它们的线来表示可比性关系. 那么有可能:  $A$  和  $C$  可以比较,  $B$  和  $C$  可以比较, 但是  $A$  和  $B$  不能比较. 人们可能会构造这样一种情况, 即  $(A|D) < (C|D)$  且  $(B|D) < (C|D)$ , 但是  $(A|D) < (B|D)$  和  $(A|D) \geqslant (B|D)$  都不成立. 这允许一种不能为每个命题分配一个实数表示 (尽管它可以用向量网格来表示) 的更宽松的结构, 任何引入单个数值表示的尝试都会产生系统中不存在的错误比较.

已经有很多努力来尝试发展这种更宽松形式的概率论. 在这些理论中, 人们不以实数表示合情性, 而只承认  $(A|C) \geqslant (B|C)$  形式的定性排序关系, 并且试图推导出具有性质 (2.85) 的 (不一定是唯一的) 可加性测度  $\rho (A|B)$  的存在. 萨维奇的工作 (Savage, 1954) 可能是这方面最著名的例子. 法恩 (Pine, 1973) 对此类尝试进行了总结. 这些努力似乎只是出于审美上的需要——普遍可比性是超出我们需要的更强的公理——而不是希望通过放弃它可以获得任何特定的实用优势. 然而, 比较概率论中出现的一个局限性使得这种尝试失去了最初的吸引力.

排序关系不能随意分配, 因为必须始终可以通过添加更多命题和排序关系来扩展话语域, 而且不产生矛盾. 如果添加新的排序关系产生不传递性, 则需要修

改一些排序关系以恢复传递性。但是这样的扩展可以无限地进行, 并且当一组具有传递排序关系的命题在从不可能到确定的路径上在某种意义上变得"到处稠密"时, 一致性将要求该理论逼近本书阐述的常规的数值概率论。

回想一下 (即考虑到考克斯的一致性定理), 这并不奇怪。如果一种比较概率论的结果与我们的数值概率论的结果相冲突, 其中必然包含明显的不一致性或存在产生不一致性的种子, 当人们试图扩展讨论域时, 这些不一致性就会变得明显。

此外, 在我们看来, 任何执行比较概率论运算的计算机必然在某个阶段将排序关系表示为实数的不等式。因此, 试图避免数值表示不仅没有实用的优势, 而且是徒劳的。比较概率论的研究最终只是向我们展示了我们在这里遵循的考克斯方法优越性的另外一个方面。

# A.4 对普遍可比性的反对

然而, 前面几节中的论证并没有完全终结这个主题, 因为作为逻辑的概率论的一些批评来自这样一些人, 他们认为假设所有命题都可以比较是荒谬的。这种观点似乎源于两种不同的信念: (1) 人脑无法做到这一点; (2) 他们认为已经展示了从根本上不可能比较所有命题的例子。

论证 (1) 对我们没有任何意义。在我们看来, 人的大脑做了很多荒谬的事情, 却没有做很多明智的事情。我们发展形式推断理论的目的不是模仿它们, 而是纠正它们。我们认同人类大脑难以比较和推断涉及不同背景的命题。但是我们也会观察到, 这种能力也会随着接受教育而提高。

例如, 假设有两个命题: (A) 东京在 2230 年 6 月 1 日发生大地震; (B) 挪威那天捕鱼会异常适合。命题 A 比命题 B 更有可能吗? 对大多数人来说, 命题 A 和命题 B 的背景似乎非常不同, 以至于我们不知道如何回答这个问题。但是, 只要稍微接受过地球物理学和天体物理学的教育, 就会意识到月球很可能会同时影响这两种现象, 因为它会导致地壳中潮汐和应力幅度的锁相周期性变化。毕竟, 认识到可能起作用的共同物理原因会使得这些命题看起来具有可比性。

上面提到的第二个对普遍可比性的反对意见似乎是对我们目前理论的误解, 但是它确实指出了普遍可比性从根本上不可能的情况。在这些情况下, 我们试图针对不止一个属性对命题进行分类, 如第 1 章末尾提到的可能的心理活动多维模型。我们看到的所谓的普遍可比性的反例无一例外都被证明是这种类型。

例如, 矿物学家可以根据两种量 (例如密度和硬度) 对一组岩石进行分类。如果在它们的某个子类中, 仅密度不同, 那么显然存在可以由实数  $d$  准确表示的可传递的可比关系。如果在另一个子类中硬度不同, 则实数  $h$  可以表示类似的可

比性. 但是, 如果我们需要同时根据两个维度对岩石进行分类, 则需要两个实数  $(d, h)$  来表示, 任何以唯一一维顺序排列它们的尝试都将是随意的.

如果引入某个新的价值判断或"目标函数"  $f(d, h)$ , 它通过诸如  $f(d_{1}, h_{1}) = f(d_{2}, h_{2})$  之类的关系告诉我们如何权衡  $d$  中的变化  $\Delta d = d_{2} - d_{1}$  和  $h$  中的变化  $\Delta h = h_{2} - h_{1}$ , 则可以消除这种随意性. 这样, 我们就又根据一个属性对岩石进行分类, 即  $f$ , 并且普遍可比性再次成为可能.

在这里发展的概率理论中, 根据定义, 我们仅根据一种属性对命题进行分类, 可直观地称之为"合情性". 一旦理解了这一点, 我们就认为用实数表示的可能性永远不会受到质疑, 并且这样做的吸引力已被该理论的所有好的结果和有用的应用所证明.

尽管如此, 比较概率论的一般思想可能在两个方面对我们有用. 首先, 出于许多目的, 人们可能不需要精确定义的数值概率, 任何在一组命题中保持排序关系的值都可能足以满足我们的需求. 如果只需要在两个相互竞争的假设或两种可行的行动之间进行选择, 那么很大范围内的数值概率值都会导致相同的最终选择. 那么该范围内的精确位置是无关紧要的, 确定它会浪费计算资源. 这样, 一种非常像比较概率论的东西将会出现, 不是作为数值概率论的推广, 而是作为对数值概率论的简单、有用的近似.

其次, 上述关于东京和挪威问题的观察显示了概率网格理论的一种可能的合理应用. 如果我们的大脑不自动具有普遍可比性的特性, 那么也许网格理论可能比拉普拉斯- 贝叶斯理论更接近描述我们实际思考的方式. 网格理论有哪些可以预期的性质?

# A.5 关于网格理论的推测

一个明显的性质是, 我们只能在由一组可比较命题组成的某个"领域"中进行合情推理. 如果涉及跨越网格的相距很远的部分, 我们不知道如何推理, 除非意识到命题之间的某种逻辑关系, 否则我们就没有比较它们合情性的标准. 在网格的不同部分, 合情性尺度可能相差很大, 除非学会增加可比性的程度, 否则我们无法知道这一点.

的确, 人脑一开始就并不是一个有效的推理机器, 无论是对于合情推理还是演绎推理. 这是我们需要多年才能学习的东西, 并且一个知识领域的专家在另一个领域可能只能做非常差的合情推理. 在学习过程中, 大脑内部发生了什么?

教育可以被定义为认识到越来越多的命题以及它们之间越来越多的逻辑关系的过程。这样, 一个似乎很自然的推测是: 一个小孩会在一个具有非常开放结构的网格上推理, 网格的大部分根本没有相互关联。例如, 历史事件中的时间关联不是自动的。我曾见过一个孩子, 他了解一些古埃及历史, 并且研究过图坦卡蒙墓中宝藏的图片, 但是放学回家却一脸疑惑地问道: "亚伯拉罕·林肯是第一个人吗?"

有人向他解释说, 埃及文物已经有 3000 多年的历史, 而亚伯拉罕·林肯在 120 年前还活着。但是这些话的意思之前并没有在他的大脑中出现。这让我们怀疑是否可能存在某种原始文化, 其中的成年人没有将时间视为超出他们自己生命的概念。如果是这样, 这一事实可能不会被人类学家发现, 因为他们根本不会提出这个问题。

随着学习的进行, 网格会发展出越来越多的点 (命题) 和相互关联的线 (可比关系), 其中的一些需要根据以后的知识进行修改以保持一致性。通过发展出具有越来越稠密结构的网格, 人们会使合情性尺度被更加严格地定义。

没有一位成年人能够达到认识所有可能命题之间关系的受教育程度, 但是他可以在某个狭窄的专业领域中达到这一程度。在该领域内, 会存在 "类普遍可比性" 他在这个领域内的合理推理将接近于拉普拉斯- 贝叶斯理论给出的推理。

一个人的大脑可能会发展出几个孤立的区域, 在这些区域中, 网格局部非常稠密。例如, 一个人可能非常了解生物化学和音乐学。这时, 对于每个单独区域内的推理, 拉普拉斯- 贝叶斯理论将非常近似, 但是仍然无法将不同区域相互关联。

那么, 当网格变得处处稠密并且具有真正的普遍可比性的极限情况时, 会发生什么? 显然, 网格会坍缩成一条直线, 所有合情性与实数的唯一联系将成为可能。因此, 拉普拉斯- 贝叶斯理论并不是描述实际人类大脑的归纳推理, 它描述了 "受过无限教育" 的大脑的理想极限情况。难怪我们不知道如何在所有问题中使用它!

这种猜测可能很容易被证明只是科幻的。然而, 我们觉得其中至少应该包含一点儿真理的成分。与所有真正基本的问题一样, 我们必须将最终的判断留给未来。

# 附录B 数学形式与风格

我们在此汇集了在整本书中使用的各种数学约定的简要说明，并讨论在概率论中出现的一些基本数学问题.在最近的文献中，粗心的记号已经导致了很多错误结果，我们需要找到合适的记号和术语的使用规则，使得人们不容易犯此类错误

数学记号，就像语言一样，本身并不是目的，而只是一种交流的工具．如果允许记号像语言一样随着使用而演变，那将是最好的．这种演变通常是采用缩写形式，可以在根据上下文了解其含义时减少符号的数量.

但是，一种鲜活、不断变化的语言仍然需要语法与拼写形式的一套固定规则作为避风港．这些规则隐藏在字典中，在可能存在歧义时使用．同样，概率论需要一套固定的规范规则，我们在有疑问时需要依靠这些规则．这里会陈述形式记号规则和逻辑层次结构，从第3章开始的所有章节都遵从这些标准记号形式，并由此演化．在某一章中方便甚至几乎是必需的符号却可能在另一章中引起混淆，所以每个单独的主题必须允许从标准记号开始独立演变.

# B.1 记号和逻辑层次结构

在我们的形式概率符号（大写  $P$  表示的那些）

$$
P(A|B) \tag{B.1}
$$

中，  $A,B$  始终代表命题．这些命题（至少对我们而言）具有足够清晰的含义，以至于我们愿意将它们作为服从布尔代数的亚里士多德逻辑的元素．因此，  $P(A|B)$ 并不是通常意义上的“函数”

我们再次强调：如果条件  $B$  在我们问题的背景中碰巧具有零概率（例如，  $B =$ $CD$  ，但  $P(C|D) = 0)$  ，概率符号是未定义且没有意义的．认识不到这一点可能会导致错误的计算——正如无意中除以一个恰好是0的表达式可能会使所有后续结果无效.

为了保持概率符号(B.1）的纯粹性，我们还必须有其他符号．因此，如果命题  $A$  具有意义

$$
A\equiv \frac{\pi}{2}\frac{\pi}{2} q\equiv \frac{\pi}{2}\frac{\pi}{2} q\equiv \frac{\pi}{2} q^{\prime}, \tag{B.2}
$$

那么通常就不写成  $P(A|B)$  ，而是倾向于写成

$$
P(q^{\prime}|B). \tag{B.3}
$$

但  $q^{\prime}$  并不是一个命题,所以作者显然想用(B.3)代表一个变量  $q^{\prime}$  的普通数学函数。但是在我们的符号系统中,这是不合法的。如果想表示普通数学函数,我们将小心地使用一个不同的函数符号,比如  $f(\mathbf{\theta}|\mathbf{\theta})$  ,将符号(B.3)写成

$$
f(q^{\prime}|B). \tag{B.4}
$$

区分符号(B.3)和(B.4)在某些读者看来可能有些迁腐,但是我们为什么要这样坚持呢?许多年前,我也会认为这一点太琐碎,不值一提。但是后来的经验表明,未清晰地加以区别会导致许多人进行错误计算并得出错误结论。这浪费了大量的时间和精力——而且这种浪费仍在概率论领域中发生——因此我们有必要采取措施来防止它重演。

关键是命题  $A$  可能确实指定某个变量  $q$  的值,也通常包含限定语句的陈述:

如果尝试在概率符号中简短地用  $q^{\prime}$  代替  $A$  ,就会忽略限定语句,在后面的计算中,相同的变量  $q^{\prime}$  可能出现在具有不同限定语句  $B_{1}$  的命题  $A_{1}$  中,人们可能会再次试图用概率符号中的  $q^{\prime}$  替换  $A_{1}$  。后来,同样的概率符号会出现两种不同的含义,人们会误以为它们代表相同的量。

这就是著名的"边缘化悖论"中发生的事情,其中相同的概率符号用来表示两个不同先验信息为条件的概率,并得出杰恩斯(Jaynes,1980)和第15章中描述的奇怪结果。这种混淆仍然会给那些尚未理解概率论的人造成麻烦。

但是,我们对这种记号法并不执着,在几乎没有错误危险的简单情况下,我们允许做一定的妥协并遵循大多数作者的习惯,即使它不是严格一致的记号。在带有小写  $p$  的概率符号中,我们将允许参数是命题、数字或者二者的任意组合:因此,如果  $A$  是命题,  $q$  是数,则等式

$$
p(A|B) = p(q|B) \tag{B.6}
$$

是被允许的,但是要注意,当使用小写  $p$  符号时,读者必须根据上下文判断它的含义,并且有可能因未能正确区分而出错。

一个常见且有用的习惯是使用希腊字母表示概率分布中的参数,使用相应的拉丁字母表示数据的相应函数。例如,可以用  $\mu = \langle x\rangle = E(x)$  表示概率均值(概率分布的平均值),而数据的平均值将是  $m = \overline{x} = n^{- 1}\sum x_{i}$  。我们坚持这一点,除非会由于与其他一些习惯用法相冲突而造成混淆。

# B.2 我们的"谨慎"策略

从第2章中根据对合理性和一致性的简单合情条件导出的概率论规则适用于离散、有限的命题集合。因此,有限集合是我们的安全港湾,其中考克斯定理适

用，并且没有人能从应用加法规则和乘法规则中产生不一致性。同样，在初等算术中，有限集合是安全港湾，没有人会通过应用加法和乘法运算产生不一致性。

我们一旦试图将概率论扩展到无限集合，就需要在数学上保持谨慎，就像人们从有限算术表达式扩展到无穷级数时那样。第15章开头的“室内游戏”的例子表明，将在有限集合上总是安全的初等算术运算与分析操作应用到无限集合上，是多么容易犯错误。

在概率论中，目前已知的唯一安全流程似乎是先通过将概率论规则严格应用于有限命题集合来推导出结果，然后在有限集合结果摆在我们面前之后，观察它在命题数量无限增加时的表现．基本上有以下三种可能.

(1) 它平滑地趋于一个有限的极限, 有些项变得越来越小并消失, 留下了一个更简单的解析表达式.(2) 它会爆炸, 即在极限时变为无限大.(3) 它保持有界, 但是会永远振荡或波动, 从不趋于任何确定的极限.在情况(1) 下, 我们说极限是“行为良好的”并接受极限是无限集合的正确解. 在情况(2) 和(3) 下, 该极限是“病态的”, 不能被视为问题的有效解. 这时我们从根本上拒绝取极限.

这就是“三思而后行”的策略：原则上，只有在验证极限行为良好后，我们才会取极限．当然，这并不意味着我们在实践中对每一个问题都会重新进行这样的检验．大多数情况会反复出现，标准情况的行为规则可以一劳永逸地使用．但是如果有疑问，我们别无选择，只能重新检验.

在极限行为良好的情况下，可以通过直接对无限集合运算来获得正确答案，但是我们不能指望这一定可行．如果极限是病态的，那么任何直接在无限集合上解决问题的尝试都会导致无意义的结果．如果我们只看极限而不是取极限的过程，则无法看出其原因．第15 章中提到的悖论说明了这方面的粗心大意所导致的一些恐怖后果

# B.3 威廉·费勒对于测度论的态度

与我们的策略相反，概率论的许多论述从一开始就试图在可数或不可数的无限集合上分配概率．那些使用测度论的人实际上是假设在引入概率之前已经完成了到无限集合的途径．例如，费勒提倡这一策略，并在其著作（Feller，1966）的第二卷中使用它

在讨论这一问题时, 费勒 (Feller, 1966) 指出, 各种应用领域的专家有时 "否认需要测度论, 因为他们不熟悉其他类型的问题, 以及模糊推理确实导致错误结果的情况". 如果费勒知道这样的事情的任何示例, 那么肯定会说明——但是他没有. 因此, 正如他所说, 我们仍然没有发现错误结果是由于未使用测度论的情况.

但是, 正如第 15 章中特别指出的, 在许多可记录的示例中对无限集合的粗心使用导致了荒谬的结果. 我们还没发现我们的 "谨慎" 策略会导致不一致、错误, 或者未能产生合理结果的情况.

我们不使用测度论的符号, 因为它预设在推导开始时已经完成了无穷极限的途径——无视第 15 章开始引用的高斯的建议. 我们经常在推导结束时取无穷极限, 实际上是在直接使用 "勒贝格测度" 的原始含义. 我们认为未能使用当前的测度论符号并不是 "模糊推理", 恰恰相反, 这是是否以正确次序做事的问题.

费勒确实不情愿地承认了我们的立场是正确的. 虽然他认为从有限集合过渡到明确定义的极限是不必要的, 但是他承认它 "在逻辑上无可挑剔" 并且具有 "对于初学者来说是一个很好的练习" 的优点. 这对我们来说已经足够了, 因为在这个领域, 我们都是初学者. 也许最需要学习的初学者是那些拒绝这种非常有指导意义的练习的人.

我们还注意到, 测度论并不总是适用的, 因为并非所有出现在实际问题中的集合都是可测的. 例如, 在许多应用中, 我们希望为事先知道是连续的函数分配概率. 但是马克·卡克 (Mark Kac, 1956) 指出存在不可测的连续函数, 它的内测度为 0 , 外测度为 1.  $①$  作为数学家, 他愿意牺牲现实世界的某些方面, 以符合这一集合应该可测的先入之见. 因此, 为了得到一个可测函数类, 他将其扩展到包括处处不连续的函数. 但是, 由此产生的测度 "几乎完全" 集中在这些处处不连续的函数类上. 出于物理原因, 我们强烈要求从我们的集合中排除这些函数! 因此, 虽然卡克得到了令他满意的解, 但这并不总是真正问题的解.

我们的价值判断恰恰相反: 关注现实世界. 我们愿意牺牲关于可测类的先入之见, 以保留现实世界中对我们的问题很重要的方面. 在这种情况下, 我们的谨慎策略的某个形式将始终能够绕过测度论以获得我们寻求的有用结果. 例如, (1) 在有限数量的  $n$  个正交函数中展开连续函数; (2) 在有限维空间  $R^{n}$  中为展开系数分配概率; (3) 做概率计算; (4) 最后传递到极限  $n \rightarrow +\infty$ . 在一个实际问题中, 我们发现将  $n$  增加到超过某个值会使我们的结论发生数值上可忽略的变化 (即如果我们正在计算有限数量的小数位, 严格来说变化为 0 ). 所以我们终究从不需要

脱离有限集合.在从统计力学到雷达侦测的各种应用中，都可以通过这种方式找到有用的结果.

在我们看来, 计算中出现的大多数 (也许是全部) 无限集合悖论是由过早地过渡到无穷极限的倾向造成的. 通常, 这意味着至关重要的信息在我们有机会使用之前就丢失了, 第 15 章中的非聚集性的情况就是一个很好的例子. 无论在何种情况下, 无论原因是什么以及有什么补救方法, 我们的观点都是, 无限集合悖论属于无限集合理论领域, 在概率论中没有立足之地. 我们对自己施加限制, 只考虑有限集合及其良好极限, 这使得我们能够避免最近统计文献中出现的所有无用和不必要的悖论. 根据这一经验, 我们推测概率论中的所有正确结果可能都是有限集合上的组合定理或它们的良好极限.

但是在这个问题上, 我们也不狂热. 我们认识到: 集合论和测度论的语言是术语上的一个有用发展, 在某些情况下使人们能够一般、简洁地陈述数学命题, 这在 19 世纪的数学中是相当缺乏的. 因此, 只要它有助于我们的目标, 我们就很高兴使用这种语言. 如果不偶尔使用 “几乎所有” 或 “零测度” 这些术语, 我们几乎无法前行. 然而, 当我们使用一点儿测度论时, 从来没有想过这会使论证更加严格, 而只是承认该语言的简洁性.

当然, 我们随时准备并且愿意使用集合论与测度论——就像我们准备并且愿意使用数论、射影几何、群论、拓扑学或任何其他数学分支一样——只要这对于找到或理解结果有所帮助. 但是, 我们认为没有必要使用集合论与测度论术语和符号陈述每个命题, 特别是在使用简单的语言更清晰的情况下. 而且据我们所知, 对我们的目的而言, 使用简单的语言会更有效, 而且实际上更安全.

事实上, 坚持对所有数学知识始终用术语表述可能会给理论带来不必要的负担, 尤其是对于一种旨在应用于现实世界的理论. 这也可能会显得比较造作, 只有语言上的作用, 而不具有实际功用. 给每一个我们熟悉的旧概念一个高斯和柯西不知道的新的令人印象深刻的名字和符号与严格无关. 它通常是一种花招, 真正目的是隐藏正在做的本质上平凡的事情. 用简单的语言陈述它会使人觉得脸红.

# B.4 克罗内克与魏尔斯特拉斯的比较

说到这里, 读者心中肯定会有一个疑问. 我们强调有限集合的安全性, 似乎整个数学分析 (一切都是在不可数集合上进行的) 都是值得怀疑的. 让我们解释一下为什么事实并非如此, 以及为什么我们对柯西和魏尔斯特拉斯的数学分析充

满信心. ①

19世纪后半叶,卡尔·魏尔斯特拉斯(1815—1897)和利奥波德·克罗内克(1823—1891)都在柏林大学讲授数学. 他们之间形成了一种差别,这种差别被后来的评论家大大夸大了. 直到最近几年,他们之间关系的真相才开始浮出水面.

简而言之,魏尔斯特拉斯致力于完善分析工具(尤其是幂级数展开),时刻不忘应用于椭圆函数的具体例子. 克罗内克更关心数论的数学基础,并质疑不从整数开始进行推理的有效性. 表面上,这似乎否定了所有美好的数学分析结果. 莫里斯·克莱茵的书(Kline,1980)给人的印象也是,克罗内克的苦行主义否定了现代数学中的一些重要进展. 但是这种记录其实歪曲了事实.

例如,贝尔(Bell,1937,第568页)将魏尔斯特拉斯描绘成伟大的数学分析大师. 他对柯西的工作进行了最后的补全,而克罗内克则只是一只牛虻,攻击魏尔斯特拉斯所做的一切工作的有效性,但是没有做出任何积极的贡献. 克罗内克确实至少有一次曾经惹恼了魏尔斯特拉斯,这在魏尔斯特拉斯的信件中有所记载. 然而,他们在原则上并没有真正的冲突. 要了解他们的观点,我们需要一位比贝尔更好的证人,幸运的是,我们有两位:亨利·庞加莱和哈罗德·爱德华兹.

1897年魏尔斯特拉斯去世时,庞加莱写了一篇对他的数学工作的总结(Poincaré,1899),其中指出:"……所有作为分析对象以及处理连续量的方程只不过是符号,取代与整数相关的无限不等式集合." 用爱德华兹(Edwards,1989)的话来说,"……魏尔斯特拉斯和克罗内克的数学都完全基于整数,因此他们所有的工作都以算术的确定性为基础". 爱德华兹还指出,通常归于克罗内克的一些保守观点只是道听途说,在克罗内克自己的话中找不到支持证据.

例如,贝尔(Bell,1937,第568页)告诉我们(这没有任何文献支持)克罗内克在听到林德曼关于  $\pi$  是超越数的证明时,问这有什么用处,因为"……无理数并不存在". 可以明确的事实是克罗内克自己关于数论方面的工作(Kronecker,1901,第4页)将莱布尼茨公式

$$
\frac{\pi}{4} = 1 - \frac{1}{3} +\frac{1}{5} -\frac{1}{7} +\dots \tag{B.7}
$$

描述为"关于奇数最优美的算术性质之一,即确定了这个几何无理数". 显然,克罗内克认为无理数至少具有足够的"存在性"以允许它们被精确定义. 的确,他并

不认为无理数是数学基础的必要组成部分。事实上,鉴于像上面那样允许完全用整数来定义无理数,他或者其他人怎么会认为无理数是基础的必要组成部分呢?奇怪的是,魏尔斯特拉斯也以同样的方式根据整数定义了无理数。那么他们之间的区别在哪里呢?

克罗内克和魏尔斯特拉斯之间的区别是审美上的而不是实质性的:克罗内克希望始终保持第一原则(起源于整数),而已经做了新构造的魏尔斯特拉斯想忘记其构造步骤,并将其用作进一步构造的元素。用现代计算机术语来说,魏尔斯特拉斯并没有否认克罗内克关于所有数学的"机器语言"基础的思想,而是想用更高级的语言发展数学分析。爱德华兹指出克罗内克的原则"……在他的思想中以及事实上,与他的前辈们——从阿基米德到高斯——的原理没有什么不同"。

幸亏有爱德华兹的历史研究,真相开始浮出水面,克罗内克被证明是无辜的且被恢复名誉。或许克罗内克过于狂热,或许他误解了魏尔斯特拉斯的立场,但从那以后的一系列事件表明他对自己的事业不够狂热。他未能回应乔治·康托尔(1845—1918)似乎很不幸,但是很容易理解。

对克罗内克来说,康托尔的想法太离谱了:它们与数学无关,数学家们没有理由关注它们。如果数学期刊的编辑们犯错误出版了这些东西,那是他们的问题,而不是他的问题。但是克罗内克的通信中确实包含了一些非常重要的真理,特别是,他抱怨说,集合论的大部分内容是幻想的,因为没法算法化(即不包含可以构造给定元素或者通过有限步骤的操作决定给定元素是否属于给定集合的规则)。今天,以我们的计算机思维,这似乎是陈词滥调,很难想象有人会忽视它,更不用说否认它了。但是这正是已经发生的事情。我们认为,如果数学家们更加关注克罗内克的这一警告,今天的数学可能会更健康。

# B.5 什么是合法数学函数?

当前纯数学和应用数学之间的很大区别在于它们对"函数"概念的不同观念。从历史上看,人们从表现良好的解析整函数出发,例如  $f(x) = x^{2}$  或  $f(x) = \sin x$ 。然后将这些"好函数"以两种不同的方式进行推广。在纯数学中,推广的原则是集合论概念仍然有效。首先是分段连续函数,然后发展到相当任意的其他规则。根据这些规则,给定一个数  $x$ ,可以定义另一个数  $f$ 。然后,意识到函数或其参数不限于是实数或复数,函数概念进一步推广到一个集合  $X$  到另一个集合  $F$  的任意映射,其中的元素几乎可以是任何东西。

在应用数学中,函数的概念以非常不同的方式推广,原则是我们对函数执行的有用的解析运算仍然有效。最重要的线索或许可以由傅里叶变换来说明。这仍

然是一种映射, 却是地更高层次上将一个函数  $f(x)$  映射到另一个函数  $F(k)$  上. 该映射通过以下积分定义:

$$
F(k) = \int \mathrm{d}x \mathrm{e}^{\mathrm{i}k x} f(x), \qquad f(x) = \frac{1}{2\pi} \int \mathrm{d}x \mathrm{e}^{-\mathrm{i}k x} F(k). \tag{B.8}
$$

如果将傅里叶变换对用符号

$$
\left[f(x) \leftrightarrow F(k)\right] \tag{B.9}
$$

表示, 我们就会发现它在平移、卷积和微分变换下的有趣性质:

$$
\left[f(x - a) \leftrightarrow \mathrm{e}^{\mathrm{i}k a} F(k)\right], \tag{B.10}
$$

$$
\left[\int \mathrm{d}y f(x - y) g(y) \leftrightarrow F(k) G(k)\right], \tag{B.11}
$$

$$
\left[f^{\prime}(x) \leftrightarrow \mathrm{i} k F(k)\right], \qquad \left[-\mathrm{i} x f(x) \leftrightarrow \mathrm{i} F^{\prime}(k)\right]. \tag{B.12}
$$

换句话说, 一个函数的解析运算对应于另一个函数的代数运算.

在实践中, 这些都是非常有用的性质. 因此, 要求解线性微分方程或差分方程, 或者卷积形式为  $\left[\int \mathrm{d}y K(x - y) f(y) = \lambda g(x)\right]$  的积分方程, 或者一个包含所有这三种运算的线性方程, 可以先对其进行傅里叶变换, 将其转换为关于  $F(k)$  的代数方程. 如果方程对于  $F(k)$  可以直接求解, 那么进行傅里叶逆变换会产生原始方程的解  $f(y)$ . 因此, 傅里叶变换将线性解析方程的解简化为普通代数方程的解. 在 20 世纪初, 慕尼黑的理论物理学家阿诺德·索末菲成为通过炫酷的轮廓积分来计算这些解的伟大艺术家. 下一代的一些最伟大的艺术家也从他那里学到了这一技术. 今天, 没有傅里叶变换, 物理学家和工程师几乎无法生存.

这个流程似乎只适用于有限的一类函数. 狄利克雷形式的傅里叶理论表明, 如果  $f(x)$  是绝对可积的, 那么积分 (B.8) 肯定会收敛到实轴上表现良好的连续函数  $F(k)$ , 并且一切安好. 如果  $f(x)$  对负  $x$  消失, 那么  $F(k)$  是解析的, 并且在二分之一的复平面上是有界的, 一切会更好. 但是如果  $f(x)$  是绝对可积的, 那么  $f^{\prime}(x)$  或  $f^{\prime \prime}(x)$  可能不是, 以上有用的性质是否仍然有效就会有一些疑问. 在关于傅里叶变换的早期工作中, 如蒂奇马付的著作 (Titchmarsh, 1937), 几乎所有注意力都集中在积分收敛理论上. 任何积分不收敛的函数都被认为不具有傅里叶变换. 这对傅里叶理论的应用范围造成了极大的限制.

随后, 在理论物理学中出现了一种更复杂的观点. 人们意识到傅里叶变换的有用性不在于任何积分的收敛, 而在于映射的上述性质 (B.10)~(B.12). 因此, 只要我们的函数表现足够好, 使得 (B.10)~(B.12) 中的运算有意义, 那么, 如果我们可以通过任何方式定义映射以保留这些性质, 通常使用傅里叶变换来求解线性

积分微分方程所得到的解将是非常严格的。无论积分 (B.8) 还是类似的傅里叶级数收敛与否, 都没有丝毫区别。发散的傅里叶级数仍然是一个唯一有序的数字序列, 传达了所有需要的信息 (即它由其傅里叶变换唯一确定, 并且有唯一确定的傅里叶变换)。这种映射最初是通过只在特殊情况下存在的级数和积分表示被发现的, 这只是一个历史偶然。

# B.5.1 德尔塔函数

虽然德尔塔函数的起源可以追溯到 19 世纪的杜哈明和格林, 但是通常被认为是从狄拉克开始的。狄拉克在 20 世纪 20 年代发明了德尔塔函数符号  $\delta (x - y)$ , 推广了克罗内克的  $\delta_{ij}$ , 并展示了如何在应用中充分利用它。它是"常数的傅里叶变换", 因为当  $F(k) \rightarrow 1$  时有  $f(x) \rightarrow \delta (x)$ 。根据"函数"的集合论定义进行思考的数学家感到震惊, 并认为这是不严谨的, 理由是德尔塔函数不"存在"。但这只是因为他们对"函数"一词的定义不恰当。德尔塔函数不是任何集合到任何其他集合的映射。洛朗·施瓦茨 (Schwartz, 1950) 试图使德尔塔函数的概念变得更严谨。但从我们的角度来看, 这很尴尬, 因为他坚持以一种不适合分析的方式定义"函数"一词。

意识到这一点, 坦普尔 (Temple, 1955) 和莱特希尔 (Lighthill, 1957) 展示了如何简单地通过将函数定义为"好"函数和好函数序列的限制来消除这种尴尬 (因此, 在我们的系统中, 一个不连续的函数定义为连续函数序列的极限)。对此, 开集和闭集之类的东西几乎不用说。莱特希尔认为, "函数"的这种定义适合于傅里叶理论。现在很明显, 它也适用于概率论和所有数学分析。有了它, 我们的定理变得更简单、更通用, 没有一长串例外和特殊情况。例如, 任何傅里叶级数现在都可以逐项微分任意次数, 无论收敛与否, 结果都表示 (通过一一对应) 我们对这个词的理解的唯一函数。早在施瓦茨、坦普尔和莱特希尔的工作之前, 物理学家就已经直观地看到这一点并正确地使用了它。

莱特希尔写了一本关于新形式傅里叶分析的非常薄的书 (Lighthill, 1957), 其中包括一张傅里叶变换表, 表中的每一条都是一个以前不具备傅里叶变换的函数。该表是线性积分微分方程的有用解的金矿。在对莱特希尔这本书的著名评论中, 理论物理学家弗里曼·戴森 (Dyson, 1958) ——剑桥数学家哈代的前学生——说莱特希尔的书"……将哈代的作品置于废墟之中, 哈代会比任何人都更喜欢它"。在本书中, 我们认为莱特希尔的方法是理所当然的, 并假设读者熟悉它。