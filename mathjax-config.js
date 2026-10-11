window.MathJax = {
    loader: {
        load: ['[tex]/ams', '[tex]/mathtools']
    },

    tex: {
        inlineMath: {
            '[+]': [['$', '$']]
        },

        packages: {
            '[+]': ['ams', 'mathtools']
        },

        macros: {
            R: "\\mathbb{R}",
            N: "\\mathbb{N}",
            Z: "\\mathbb{Z}",
            Q: "\\mathbb{Q}",

            E: "\\mathbb{E}",
            P: "\\mathbb{P}",

            Var: "\\operatorname{Var}",
            Cov: "\\operatorname{Cov}",
            Corr: "\\operatorname{Corr}",

            argmax: "\\operatorname*{arg\\,max}",
            argmin: "\\operatorname*{arg\\,min}"
        }
    }
};